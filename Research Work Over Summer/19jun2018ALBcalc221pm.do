// read this program with the Alberta Tax Credit Form 
// the form asks what field of science the coroporation is in, but this program ignores that for now
// 4 June 2018 
program albertaITC, rclass 
	args totalEx albertaEx albertaDe albertaPr albertaCr albertaAs associated startDate endDate allocatedLim recapture previousYrExp previousYrLim previousFedExp previousYrDeduct previousYrFedCred 
	local eligibleEx=`albertaEx'-`albertaDe'+`albertaPr'+`albertaCr'+`albertaAs'
	//rename variable to elgibileAlbertaEx
	
	local daysTax=td(`endDate')-td(`startDate')
	
	local expenditureLimit=0
	//place holder value
	if `associated'==1 {
		local dayRatio=`daysTax'/365
		if inrange(td(29feb2000),td(`startDate'),td(`endDate')) | inrange(td(29feb2004),td(`startDate'),td(`endDate'))==1 | inrange(td(29feb2008),td(`startDate'),td(`endDate'))==1 | inrange(td(29feb2012),td(`startDate'),td(`endDate'))==1 | inrange(td(29feb2016),td(`startDate'),td(`endDate'))==1 {
		//making use of the builtin inrange(z,a,b) function, which equals one if a<=z<=b
			local dayRatio=`daysTax'/366
			}
		local expenditureLimit= 4000000*`dayRatio'
		assert `allocatedLim'<=`expenditureLimit'
		if `allocatedLim'<=`expenditureLimit' {
			`expenditureLimit'=`allocatedLim'
			}
		/*basically if the cooperation is associated, its maximum allocation limit is a portion of the overall expenditure limit */
		}
	
	if `associated'==0 { /*if the coroporation is not associated */
		assert `allocatedLim'==0
		local dayRatio=`daysTax'/365
		
		if inrange(td(29feb2000),td(`startDate'),td(`endDate')) | inrange(td(29feb2004),td(`startDate'),td(`endDate'))==1 | inrange(td(29feb2008),td(`startDate'),td(`endDate'))==1 | inrange(td(29feb2012),td(`startDate'),td(`endDate'))==1 | inrange(td(29feb2016),td(`startDate'),td(`endDate'))==1 {
		//making use of the builtin inrange(z,a,b) function, which equals one if a<=z<=b
			local dayRatio=`daysTax'/366
			}
		
		local expenditureLimit= 4000000*`dayRatio'
		
		}
	local calculate=min(`eligibleEx',`expenditureLimit')*0.1
	local taxCredit=`calculate'-`recapture'
	
	local supplemental=0
	if td(`startDate')<td(12mar2012) {
		assert `previousFedExp'==0
		assert `previousYrDeduct'==0
		assert `previousYrExp'==0
		assert `previousYrFedCred'==0
		assert `previousYrLim'==0
		}
		
	if td(`startDate')>=td(12mar2012) {
		local lesser=min(`previousYrExp',`previousYrLim')  //following the precedure from the supplemental form line from line... forgive vague variable names, could not think of anything better
		local numberfromForm=`previousFedExp'*`previousYrExp'/`previousYrLim'  
		//this number came from line 406
		local lesser_1=min(`lesser',`numberfromForm')*0.35 //made two steps into one from the form
		local subtraction=`previousYrExp'-`numberfromForm'
		local greater=max(0,`subtraction')
		local subtraction_1=`previousYrLim'-`numberfromForm'
		local line420=max(0,`subtraction_1')
		local line422=`line420'*0.20
		local add=`lesser_1'+`line422'
		local division=`previousYrDeduct'/`previousYrFedCred'
		local supplemental=`add'*`division'
		}
	
	
	
	local netRepaymentCredit=`taxCredit'-`supplemental'	
	
	/*local nonRefundable=`taxCredit'-`netRepaymentCredit'*/
	//intuition that nonRefundable credit is total credit minus refundable credit
	return scalar ITC=`taxCredit'
	return scalar repaymentITC=`netRepaymentCredit'
	/*return scalar nonrefundableITC=`nonRefundable'*/
end
	
//testing
	
albertaITC 10000 3000 500 600 400 1000 0 3jan2000 3jan2001 0 50	0 0 0 0 0 
assert r(ITC)==400
	


   