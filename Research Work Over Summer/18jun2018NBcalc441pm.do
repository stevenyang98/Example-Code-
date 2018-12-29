//18 june 2018
//New Brunswick Calculator 
program NewBrunswick,rclass
	args taxyrStart totalExpend precedingyrCredit expiredCredit transferCredit partnerCredit trustCredit totalEligibleCreditAfter  partnerReCredit trustReCredit carryfowardpryr
	
	/* so people know to use other program for years before 2003 */
	if td(`taxyrStart')<td(1jan2003) {
		assert `totalEligibleCreditAfter'==0
		assert `partnerReCredit'==0
		assert `trustCredit'==0
		} 
		/*if before 2003, these terms don't exist */
	local beginyrCredit=`precedingyrCredit'-`expiredCredit'
	local rateCredit=`totalExpend'*0.10
	local totalCredit=`beginyrCredit'+`rateCredit'+`partnerCredit'+`trustCredit'
	
	
	
	
	if td(`taxyrStart')>td(1jan2003) {
	
		local totalYrReCredit=`totalEligibleCreditAfter'*0.15
		local totalReCredit=`totalYrReCredit'+`partnerReCredit'+`trustReCredit'
	}
	/*calculate refundable credit only if year after 2003 */
	local carryforward = `carryfowardpryr'-`expiredCredit'+`totalCredit'
	return scalar nonRefundableITC=`totalCredit'
	return scalar RefundableITC=`totalReCredit'
	return scalar carryforward=`carryforward'
end
	
/*testing*/
NewBrunswick 31dec2002 10000 15000 7000 4000 3000 3000 0 0 0 3000
assert r(carryforward)==11000
	