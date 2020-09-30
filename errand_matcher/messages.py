import errand_matcher.helper as helper

def welcome_new_volunteer(volunteer):
	tiny_faq_url = helper.make_tiny_url("{}#above-faq".format(helper.get_base_url()))

	message = "Welcome to #TeamLivelyHood! We’ll text you when somebody nearby needs your help. If you ever need assistance, you can reach us here."\
	"\n\nMessage and data rates may apply. Reply STOP to opt-out of messages".format(tiny_faq_url)

	helper.send_sms(helper.format_mobile_number(volunteer.mobile_number), message)


def send_otp(user_otp):
	message = "LivelyHood here! {} is your one-time password for online login. Please do not share.".format(
		user_otp.token)
	helper.send_sms(helper.format_mobile_number(user_otp.mobile_number), message)


def alert_volunteer_to_claim_errand(errand, volunteer):
	url = "{}/errand/{}/accept/{}".format(
		helper.get_base_url(), 
		errand.id, 
		helper.strip_mobile_number(volunteer.mobile_number))

	deadline_str = helper.convert_errand_deadline_to_str(errand)

	message = "LivelyHood here! {} needs help getting groceries! Can you make a delivery by {}? "\
			  "Click here for more information and to let us know if you can help. {}".format(
				errand.requestor.user.first_name, deadline_str, url)

	helper.send_sms(helper.format_mobile_number(volunteer.mobile_number), message)

def confirm_successful_claim(errand, volunteer):
    url = "{}/errand/{}/status/{}".format(helper.get_base_url(), errand.id, errand.access_id)
    message = "Thanks for accepting this request! See details at {}".format(url)
    helper.send_sms(helper.format_mobile_number(volunteer.mobile_number), message)


def remind_volunteer_to_complete(errand, volunteer):
	url = "{}/errand/{}/status/{}".format(helper.get_base_url(), errand.id, errand.access_id)
	message = "LivelyHood here! Just checking in on the progress of this delivery."\
	" Click here to see the details again or let us know if you’ve completed it! {} Thank you!".format(url)
	helper.send_sms(helper.format_mobile_number(volunteer.mobile_number), message)


def thank_and_survey(volunteer):
	message = "Thank you for helping a neighbor today! You made someone’s day with your gesture."\
	" Please take a minute to complete this survey so we continue to help more people."\
	" Click here for survey: https://forms.gle/ZKd5z3obSFvyejA49."\
	"\n\nWe hope you will volunteer with LivelyHood again!"
	helper.send_sms(helper.format_mobile_number(volunteer.mobile_number), message)


def alert_staff_of_unclaimed_errand(errand):
	message = 'Errand unclaimed! {} {}: {} requested at {}'.format(
                errand.requestor.user.first_name, 
                errand.requestor.user.last_name,
                helper.strip_mobile_number(errand.requestor.mobile_number),
                errand.requested_time)
	staff_number = helper.format_mobile_number(helper.get_support_mobile_number())
	helper.send_sms(staff_number, message)
