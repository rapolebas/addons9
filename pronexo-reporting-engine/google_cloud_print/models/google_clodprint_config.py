# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, _, SUPERUSER_ID
from openerp.exceptions import RedirectWarning, Warning
import werkzeug.urls
import urllib2
import logging
import json
import time
import base64
import mimetypes
import mimetools

# from https://developers.google.com/cloud-print/docs/pythonCode
BOUNDARY = mimetools.choose_boundary()
CRLF = '\r\n'
CLOUDPRINT_URL = 'https://www.google.com/cloudprint'

# this two are parameters of google_account on v9
GOOGLE_TOKEN_ENDPOINT = "https://accounts.google.com/o/oauth2/token"
TIMEOUT = 20

_logger = logging.getLogger(__name__)


class GoogleCloudprintConfig(models.Model):
    _name = 'google.cloudprint.config'

    @api.model
    def get_access_token(self, scope=None, user=None):
        """
        Return an access_token for user or use credentials stored on parameter
        """
        Config = self.env['ir.config_parameter']
        if not user:
            google_cloudprint_refresh_token = Config.sudo().get_param(
                'google_cloudprint_refresh_token')
            user_is_admin = self.env.user.id == SUPERUSER_ID
            if not google_cloudprint_refresh_token:
                if user_is_admin:
                    dummy, action_id = self.env[
                        'ir.model.data'].get_object_reference(
                        'base_setup', 'action_general_configuration')
                    msg = _(
                        "You haven't configured 'Authorization Code' generated"
                        " from google, Please generate and configure it .")
                    raise RedirectWarning(
                        msg, action_id, _('Go to the configuration panel'))
                else:
                    raise Warning(_(
                        "Google Drive is not yet configured. "
                        "Please contact your administrator."))
        else:
            google_cloudprint_refresh_token = user.google_cloudprint_rtoken

        google_cloudprint_client_id = Config.sudo().get_param(
            'google_cloudprint_client_id')
        google_cloudprint_client_secret = Config.sudo().get_param(
            'google_cloudprint_client_secret')

        # For Getting New Access Token With help of old Refresh Token
        data = werkzeug.url_encode({
            'client_id': google_cloudprint_client_id,
            'refresh_token': google_cloudprint_refresh_token,
            'client_secret': google_cloudprint_client_secret,
            'grant_type': "refresh_token",
            'scope': scope or 'https://www.googleapis.com/auth/cloudprint'
        })
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        try:
            req = urllib2.Request(GOOGLE_TOKEN_ENDPOINT, data, headers)
            content = urllib2.urlopen(req, timeout=TIMEOUT).read()
        except urllib2.HTTPError:
            if user_is_admin:
                dummy, action_id = self.env[
                    'ir.model.data'].get_object_reference(
                        'base_setup', 'action_general_configuration')
                msg = _(
                    "Something went wrong during the token generation. "
                    "Please request again an authorization code .")
                raise RedirectWarning(
                    msg, action_id, _('Go to the configuration panel'))
            else:
                raise Warning(_(
                    "Google Drive is not yet configured. "
                    "Please contact your administrator."))
        content = json.loads(content)
        return content.get('access_token')

    @api.model
    def get_response(self, interface, params=None, data=None, user=None):
        access_token = self.get_access_token(user=user)
        request_url = "%s/%s" % (CLOUDPRINT_URL, interface)
        if params:
            request_url += "?%s" % (
                werkzeug.url_encode(params))
        headers = {
            "Authorization": 'Bearer ' + access_token,
        }
        data_json = json.dumps(data)
        # _logger.info('Running GCP request with url %s' % request_url)
        try:
            req = urllib2.Request(request_url, data_json, headers)
            response = urllib2.urlopen(req, timeout=TIMEOUT).read()
        except urllib2.HTTPError:
            raise Warning(_(
                "Could not connect to google cloud print. "
                "Check your configuration"))
        # _logger.info('Google Cloud Print response for %s\n%s' % (
        #     interface, response))
        return json.loads(response)

    @api.model
    def get_printers(self, user=None):
        """
        Return a dictionary with gc printers
        """
        return self.get_response('search', user=user).get('printers')

    # este metodo es parcialmente una copia de
    # https://developers.google.com/cloud-print/docs/pythonCode
    @api.model
    def submit_job(self, printerid, jobtype, jobsrc, options):
        """Submit a job to printerid with content of dataUrl.

        Args:
            printerid: string, the printer id to submit the job to.
            jobtype: string, must match the dictionary keys in content and
                content_type.
            jobsrc: string, points to source for job. Could be a pathname or
                id string.
        Returns:
            boolean: True = submitted, False = errors.
        """

        # TODO implementar options
        if jobtype in ['qweb-pdf', 'pdf', 'aeroo']:
            jobtype = 'pdf'
        if jobtype == 'pdf':
            b64file = self.Base64Encode(jobsrc)
            fdata = self.ReadFile(b64file)
        elif jobtype in ['png', 'jpeg']:
            b64file = self.Base64Encode(jobsrc)
            fdata = self.ReadFile(b64file)
        else:
            raise Warning(_(
                'Jobtype %s not implemented for google cloud printin') % (
                jobtype))

        access_token = self.get_access_token()

        # Make the title unique for each job, since the printer by default will
        # name the print job file the same as the title.
        datehour = time.strftime('%b%d%H%M', time.localtime())
        title = '%s%s' % (datehour, jobsrc)

        # """The following dictionaries expect a certain kind of data in
        # jobsrc, depending on jobtype:
        #    jobtype               jobsrc
        #    ======================================
        #    pdf                    pathname to the pdf file
        #    png                    pathname to the png file
        #    jpeg                   pathname to the jpeg file
        #    =======================================
        # """

        request_url = "%s/%s" % (CLOUDPRINT_URL, 'submit')
        request = urllib2.Request(request_url)
        request.add_header("Authorization", 'Bearer %s' % access_token)
        content = {
            'pdf': fdata,
            'jpeg': jobsrc,
            'png': jobsrc,
        }
        content_type = {
            'pdf': 'dataUrl',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
        }
        headers = [
            ('printerid', printerid),
            ('title', title),
            ('content', content[jobtype]),
            ('contentType', content_type[jobtype])]
        files = [('capabilities', 'capabilities', '{"capabilities":[]}')]
        if jobtype in ['pdf', 'jpeg', 'png']:
            files.append(('content', jobsrc, fdata))

        data = self.EncodeMultiPart(
            headers, files, file_type=content_type[jobtype])

        request.add_header('Content-Length', str(len(data)))
        # parecen no necesarios
        # request.add_header('X-CloudPrint-Proxy', 'api-prober')
        # request.add_header('Host', 'www.google.com')
        request.add_data(data)
        request.add_header(
            'Content-Type', 'multipart/form-data;boundary=%s' % BOUNDARY)

        response = urllib2.urlopen(request).read()
        status = self.Validate(response)
        if not status:
            error_msg = self.GetMessage(response)
            raise Warning(_(
                'Print job %s failed with %s', jobtype, error_msg))
        return status

# methods from https://developers.google.com/cloud-print/docs/pythonCode
    @api.model
    def Validate(self, response):
        """Determine if JSON response indicated success."""
        if response.find('"success": true') > 0:
            return True
        else:
            return False

    @api.model
    def GetMessage(self, response):
        """Extract the API message from a Cloud Print API json response.

        Args:
            response: json response from API request.
        Returns:
            string: message content in json response.
        """
        lines = response.split('\n')
        for line in lines:
            if '"message":' in line:
                msg = line.split(':')
                return msg[1]
        return None

    @api.model
    def EncodeMultiPart(self, fields, files, file_type='application/xml'):
        """Encodes list of parameters and files for HTTP multipart format.

        Args:
          fields: list of tuples containing name and value of parameters.
          files: list of tuples containing param name, filename, and file
                contents.
          file_type: string if file type different than application/xml.
        Returns:
          A string to be sent as data for the HTTP post request.
        """
        lines = []
        for (key, value) in fields:
            lines.append('--' + BOUNDARY)
            lines.append('Content-Disposition: form-data; name="%s"' % key)
            lines.append('')  # blank line
            lines.append(value)
        for (key, filename, value) in files:
            lines.append('--' + BOUNDARY)
            lines.append(
                'Content-Disposition: form-data; name="%s"; filename="%s"'
                % (key, filename))
            lines.append('Content-Type: %s' % file_type)
            lines.append('')  # blank line
            lines.append(value)
        lines.append('--' + BOUNDARY + '--')
        lines.append('')  # blank line
        return CRLF.join(lines)

    @api.model
    def Base64Encode(self, pathname):
        """Convert a file to a base64 encoded file.
          Args:
            pathname: path name of file to base64 encode..
          Returns:
            string, name of base64 encoded file.
          For more info on data urls, see:
            http://en.wikipedia.org/wiki/Data_URI_scheme
        """
        b64_pathname = pathname + '.b64'
        file_type = mimetypes.guess_type(pathname)[0] or 'application/pdf'

        data = self.ReadFile(pathname)

        # Convert binary data to base64 encoded data.
        # file_type = 'application/pdf'
        header = 'data:%s;base64,' % file_type
        b64data = header + base64.b64encode(data)

        if self.WriteFile(b64_pathname, b64data):
            return b64_pathname
        else:
            return None

    @api.model
    def ReadFile(self, pathname):
        """Read contents of a file and return content.
           Args:
             pathname: string, (path)name of file.
           Returns:
           string: contents of file.
        """
        try:
            f = open(pathname, 'rb')
            try:
                s = f.read()
            except IOError, e:
                _logger.info('Error reading %s\n%s', pathname, e)
            finally:
                f.close()
                return s
        except IOError, e:
            _logger.error('Error opening %s\n%s', pathname, e)
            return None

    @api.model
    def WriteFile(self, file_name, data):
        """Write contents of data to a file_name.
          Args:
            file_name: string, (path)name of file.
            data: string, contents to write to file.
          Returns:
            boolean: True = success, False = errors.
        """
        status = True

        try:
            f = open(file_name, 'wb')
            try:
                f.write(data)
            except IOError, e:
                # logger.error('Error writing %s\n%s', file_name, e)
                status = False
            finally:
                f.close()
        except IOError, e:
            _logger.error('Error opening %s\n%s', file_name, e)
            status = False
        return status
