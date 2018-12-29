//18 June 2018
//British Columbia Tax Form Calculator
program BritishColumbia, rclass
	args taxYrStart CCPC currentBCExp capitalBCExp eligibleRP ccpcExpLim refundableClaim renouncedCredit creditbeginYr transferCr partnerCredit recaptureCredit previousyrcarry expiredCred
	local qualifiedSRED=`currentBCExp'+`eligibleRP'
	
	local refundableITC=0
	//changes if the company is CCPC
	if `CCPC'==1 {
		local refundableITC=min(`ccpcExpLim',`qualifiedSRED')*0.10
		}
	assert `refundableClaim'<=`refundableITC'
	
	if td(`taxYrStart')<td(1jan2008) {
		assert `partnerCredit'==0
		assert `recaptureCredit'==0
		local BCSREDyr=`qualifiedSRED'*0.10
		local deduct=`refundableClaim'+`renouncedCredit'
		local annualnrITC=`BCSREDyr'-`deduct'
		local add=`creditbeginYr'+`transferCr'
		local availableforDeduction=`annualnrITC'+`add'
		}
	
	if td(`taxYrStart')>td(1jan2008) {
		local BCSREDyr=`qualifiedSRED'*0.10
		local deduct=`partnerCredit'-`recaptureCredit'
			if `deduct'<0 {
				`deduct'=0
				/*following the form directions*/
				}
		local line20=`refundableClaim'+`renouncedCredit'
		local annualnrITC=`BCSREDyr'+`deduct'+`line20'
		}
	
	
	local carryforward=`previousyrcarry'-`expiredCred'+`annualnrITC'
	
	return scalar refundableITC=`refundableITC'
	return scalar nonrefunableITC=`annualnrITC'
	return scalar carryfoward=`carryforward'
end

//testing
BritishColumbia 2jan2007 1 10000 8000 5000 9000 600 800 8000 2000 0 0 8000
assert r(carryforward)==7900


// report Update, then to provinces:Credit rate, what happens, treats CCPCs or associated, if refundable or carryfoward, interesting features 