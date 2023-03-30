# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


import json

import dontmanage
import tweepy
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import get_url_to_form
from dontmanage.utils.file_manager import get_file_path
from tweepy.error import TweepError


class TwitterSettings(Document):
	@dontmanage.whitelist()
	def get_authorize_url(self):
		callback_url = (
			"{0}/api/method/dontmanageerp.crm.doctype.twitter_settings.twitter_settings.callback?".format(
				dontmanage.utils.get_url()
			)
		)
		auth = tweepy.OAuthHandler(
			self.consumer_key, self.get_password(fieldname="consumer_secret"), callback_url
		)
		try:
			redirect_url = auth.get_authorization_url()
			return redirect_url
		except tweepy.TweepError as e:
			dontmanage.msgprint(_("Error! Failed to get request token."))
			dontmanage.throw(
				_("Invalid {0} or {1}").format(dontmanage.bold("Consumer Key"), dontmanage.bold("Consumer Secret Key"))
			)

	def get_access_token(self, oauth_token, oauth_verifier):
		auth = tweepy.OAuthHandler(self.consumer_key, self.get_password(fieldname="consumer_secret"))
		auth.request_token = {"oauth_token": oauth_token, "oauth_token_secret": oauth_verifier}

		try:
			auth.get_access_token(oauth_verifier)
			self.access_token = auth.access_token
			self.access_token_secret = auth.access_token_secret
			api = self.get_api()
			user = api.me()
			profile_pic = (user._json["profile_image_url"]).replace("_normal", "")

			dontmanage.db.set_value(
				self.doctype,
				self.name,
				{
					"access_token": auth.access_token,
					"access_token_secret": auth.access_token_secret,
					"account_name": user._json["screen_name"],
					"profile_pic": profile_pic,
					"session_status": "Active",
				},
			)

			dontmanage.local.response["type"] = "redirect"
			dontmanage.local.response["location"] = get_url_to_form("Twitter Settings", "Twitter Settings")
		except TweepError as e:
			dontmanage.msgprint(_("Error! Failed to get access token."))
			dontmanage.throw(_("Invalid Consumer Key or Consumer Secret Key"))

	def get_api(self):
		# authentication of consumer key and secret
		auth = tweepy.OAuthHandler(self.consumer_key, self.get_password(fieldname="consumer_secret"))
		# authentication of access token and secret
		auth.set_access_token(self.access_token, self.access_token_secret)

		return tweepy.API(auth)

	def post(self, text, media=None):
		if not media:
			return self.send_tweet(text)

		if media:
			media_id = self.upload_image(media)
			return self.send_tweet(text, media_id)

	def upload_image(self, media):
		media = get_file_path(media)
		api = self.get_api()
		media = api.media_upload(media)

		return media.media_id

	def send_tweet(self, text, media_id=None):
		api = self.get_api()
		try:
			if media_id:
				response = api.update_status(status=text, media_ids=[media_id])
			else:
				response = api.update_status(status=text)

			return response

		except TweepError as e:
			self.api_error(e)

	def delete_tweet(self, tweet_id):
		api = self.get_api()
		try:
			api.destroy_status(tweet_id)
		except TweepError as e:
			self.api_error(e)

	def get_tweet(self, tweet_id):
		api = self.get_api()
		try:
			response = api.get_status(tweet_id, trim_user=True, include_entities=True)
		except TweepError as e:
			self.api_error(e)

		return response._json

	def api_error(self, e):
		content = json.loads(e.response.content)
		content = content["errors"][0]
		if e.response.status_code == 401:
			self.db_set("session_status", "Expired")
			dontmanage.db.commit()
		dontmanage.throw(
			content["message"],
			title=_("Twitter Error {0} : {1}").format(e.response.status_code, e.response.reason),
		)


@dontmanage.whitelist(allow_guest=True)
def callback(oauth_token=None, oauth_verifier=None):
	if oauth_token and oauth_verifier:
		twitter_settings = dontmanage.get_single("Twitter Settings")
		twitter_settings.get_access_token(oauth_token, oauth_verifier)
		dontmanage.db.commit()
	else:
		dontmanage.local.response["type"] = "redirect"
		dontmanage.local.response["location"] = get_url_to_form("Twitter Settings", "Twitter Settings")
