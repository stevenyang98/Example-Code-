/*This program will look at the Yukon Tax Form. Only outputs refundable ITC*/
program Yukon, rclass
	args totalexp  credPartner credTrust yukonCollegeExpend
	
	/* local creditlimit = 3000000 */
	
	/*local refundable_credit_a = 0  placeholder variable */
	
	/*local refundable_credit_b = `credPartner'*0.4*0.15
	this must be done within the fiscal year or it becomes null 
	local refundable_credit_c = `credTrust'*0.4*0.15 
	ignore this for now */
		
	local credit_yukon = `yukonCollegeExpend'*0.05
	
	
	
	local refundable_credit_a = `totalexp'*0.15
			
	local reITC = `refundable_credit_a'+`credit_yukon'+`credPartner'+`credTrust'
	return scalar reITCYukon = reITC
end

//testing
Yukon 10000 3000 4000 2000
assert r(reITCYukon)==8600


	
	
		
		
		
		
		
		
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

