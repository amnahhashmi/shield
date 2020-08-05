import errand_matcher.helper as helper

def alert_staff_of_unclaimed_errand(errand):
	message = 'Errand unclaimed! {} {}: {} requested at {}'.format(
                errand.requestor.user.first_name, 
                errand.requestor.user.last_name,
                helper.strip_mobile_number(errand.requestor.mobile_number),
                errand.requested_time)
	staff_number = helper.format_mobile_number(helper.get_support_mobile_number())
	helper.send_sms(staff_number, message)

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