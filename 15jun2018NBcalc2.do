//15 june 2018
//New Brunswick Calculator years after 2003
program NewBrunswick2003,rclass
	args taxYrEnd totalEligibleExpend precedingNonCredit expiredNonCredit transferedNonCredit partnerNonCredit trustNonCredit totalEligibleCreditAfter  partnerReCredit trustReCredit
	assert td(`taxYrEnd')>(1jan2003)
	/* so people know to use other program for years before 2003 */
	local beginyrCredit=`precedingNonCredit'-`expiredNonCredit'
	local rateCredit=`totalEligibleExpend'*0.10
	local totalNonCredit=`beginyrCredit'+`rateCredit'+`partnerNonCredit'+`trustNonCredit'
	
	local totalYrReCredit=`totalEligibleCreditAfter'*0.15
	local totalReCredit=`totalYrReCredit'+`partnerReCredit'+`trustReCredit'
	
	local totalCredit=`totalNonCredit'+`totalReCredit'
	return scalar nonRefundableITC=`totalNonCredit'
	return scalar RefundableITC=`totalReCredit'
	return scalar ITC=`totalCredit'
	