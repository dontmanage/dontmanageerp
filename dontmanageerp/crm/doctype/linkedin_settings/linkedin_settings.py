# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


from urllib.parse import urlencode

import dontmanage
import requests
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import get_url_to_form
from dontmanage.utils.file_manager import get_file_path


class LinkedInSettings(Document):
	@dontmanage.whitelist()
	def get_authorization_url(self):
		params = urlencode(
			{
				"response_type": "code",
				"client_id": self.consumer_key,
				"redirect_uri": "{0}/api/method/dontmanageerp.crm.doctype.linkedin_settings.linkedin_settings.callback?".format(
					dontmanage.utils.get_url()
				),
				"scope": "r_emailaddress w_organization_social r_basicprofile r_liteprofile r_organization_social rw_organization_admin w_member_social",
			}
		)

		url = "https://www.linkedin.com/oauth/v2/authorization?{}".format(params)

		return url

	def get_access_token(self, code):
		url = "https://www.linkedin.com/oauth/v2/accessToken"
		body = {
			"grant_type": "authorization_code",
			"code": code,
			"client_id": self.consumer_key,
			"client_secret": self.get_password(fieldname="consumer_secret"),
			"redirect_uri": "{0}/api/method/dontmanageerp.crm.doctype.linkedin_settings.linkedin_settings.callback?".format(
				dontmanage.utils.get_url()
			),
		}
		headers = {"Content-Type": "application/x-www-form-urlencoded"}

		response = self.http_post(url=url, data=body, headers=headers)
		response = dontmanage.parse_json(response.content.decode())
		self.db_set("access_token", response["access_token"])

	def get_member_profile(self):
		response = requests.get(url="https://api.linkedin.com/v2/me", headers=self.get_headers())
		response = dontmanage.parse_json(response.content.decode())

		dontmanage.db.set_value(
			self.doctype,
			self.name,
			{
				"person_urn": response["id"],
				"account_name": response["vanityName"],
				"session_status": "Active",
			},
		)
		dontmanage.local.response["type"] = "redirect"
		dontmanage.local.response["location"] = get_url_to_form("LinkedIn Settings", "LinkedIn Settings")

	def post(self, text, title, media=None):
		if not media:
			return self.post_text(text, title)
		else:
			media_id = self.upload_image(media)

			if media_id:
				return self.post_text(text, title, media_id=media_id)
			else:
				self.log_error("LinkedIn: Failed to upload media")

	def upload_image(self, media):
		media = get_file_path(media)
		register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
		body = {
			"registerUploadRequest": {
				"recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
				"owner": "urn:li:organization:{0}".format(self.company_id),
				"serviceRelationships": [
					{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}
				],
			}
		}
		headers = self.get_headers()
		response = self.http_post(url=register_url, body=body, headers=headers)

		if response.status_code == 200:
			response = response.json()
			asset = response["value"]["asset"]
			upload_url = response["value"]["uploadMechanism"][
				"com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
			]["uploadUrl"]
			headers["Content-Type"] = "image/jpeg"
			response = self.http_post(upload_url, headers=headers, data=open(media, "rb"))
			if response.status_code < 200 and response.status_code > 299:
				dontmanage.throw(
					_("Error While Uploading Image"),
					title="{0} {1}".format(response.status_code, response.reason),
				)
				return None
			return asset

		return None

	def post_text(self, text, title, media_id=None):
		url = "https://api.linkedin.com/v2/shares"
		headers = self.get_headers()
		headers["X-Restli-Protocol-Version"] = "2.0.0"
		headers["Content-Type"] = "application/json; charset=UTF-8"

		body = {
			"distribution": {"linkedInDistributionTarget": {}},
			"owner": "urn:li:organization:{0}".format(self.company_id),
			"subject": title,
			"text": {"text": text},
		}

		reference_url = self.get_reference_url(text)
		if reference_url:
			body["content"] = {"contentEntities": [{"entityLocation": reference_url}]}

		if media_id:
			body["content"] = {"contentEntities": [{"entity": media_id}], "shareMediaCategory": "IMAGE"}

		response = self.http_post(url=url, headers=headers, body=body)
		return response

	def http_post(self, url, headers=None, body=None, data=None):
		try:
			response = requests.post(url=url, json=body, data=data, headers=headers)
			if response.status_code not in [201, 200]:
				raise

		except Exception as e:
			self.api_error(response)

		return response

	def get_headers(self):
		return {"Authorization": "Bearer {}".format(self.access_token)}

	def get_reference_url(self, text):
		import re

		regex_url = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
		urls = re.findall(regex_url, text)
		if urls:
			return urls[0]

	def delete_post(self, post_id):
		try:
			response = requests.delete(
				url="https://api.linkedin.com/v2/shares/urn:li:share:{0}".format(post_id),
				headers=self.get_headers(),
			)
			if response.status_code != 200:
				raise
		except Exception:
			self.api_error(response)

	def get_post(self, post_id):
		url = "https://api.linkedin.com/v2/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:{0}&shares[0]=urn:li:share:{1}".format(
			self.company_id, post_id
		)

		try:
			response = requests.get(url=url, headers=self.get_headers())
			if response.status_code != 200:
				raise

		except Exception:
			self.api_error(response)

		response = dontmanage.parse_json(response.content.decode())
		if len(response.elements):
			return response.elements[0]

		return None

	def api_error(self, response):
		content = dontmanage.parse_json(response.content.decode())

		if response.status_code == 401:
			self.db_set("session_status", "Expired")
			dontmanage.db.commit()
			dontmanage.throw(content["message"], title=_("LinkedIn Error - Unauthorized"))
		elif response.status_code == 403:
			dontmanage.msgprint(_("You didn't have permission to access this API"))
			dontmanage.throw(content["message"], title=_("LinkedIn Error - Access Denied"))
		else:
			dontmanage.throw(response.reason, title=response.status_code)


@dontmanage.whitelist(allow_guest=True)
def callback(code=None, error=None, error_description=None):
	if not error:
		linkedin_settings = dontmanage.get_doc("LinkedIn Settings")
		linkedin_settings.get_access_token(code)
		linkedin_settings.get_member_profile()
		dontmanage.db.commit()
	else:
		dontmanage.local.response["type"] = "redirect"
		dontmanage.local.response["location"] = get_url_to_form("LinkedIn Settings", "LinkedIn Settings")
