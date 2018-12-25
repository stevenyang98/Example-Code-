//24 June 2018
//Ontario OITC
//We do not have anything before 2005...
program OITC,rclass
	args taxYrStart taxYrEnd taxable assocTaxable associated tax2003start tax2003end tax2004start 
		tax2004end tax2005start tax2005end tax2006start tax2006end assocBusinessLim assocMaxBusiness paidUp assocpaidUp currentEx capitalEx capitalRe currentRe equipmentRe
		taxableIncome taxableIncomeAssoc specifiedCapital eligibleRepaymentYears eligibleRepayementsAfter eligibleRepayementsBefore
	
	local OITC=0 
	if td(`taxYrEnd')<=td(31dec2004) {
		return local OITC "Forms prior to 2005 not found yet"
		}
 
	if td(`taxYrEnd')>td(31dec2004) {
		//assert all assoc var==0
		assert `capitalRe'==0
		assert `currentRe'==0
		local line5020=`taxable'
		//calculating line 5044 
		local divisor=td(`taxYrEnd')-td(`taxYrStart')
		local dividend2003=td(`tax2003end')-td(`tax2003start')
		local dividend2004=td(`tax2004end')-td(`tax2004start')
		local line57011=`dividend2003'/`divisor'*225000
		local line57012=`dividend2004'/`divisor'*250000
		local line5701=`line57011'+`line57012'+300000
		local maxBusinessLimit=`line5071'
		//now for business limit, which was confusing
		//my interpretation of Schedule 23 - it is a percentage of the total limit, 
		local businessLim=`line5071'
		
		if ccpc==0{
			assert `tax2003end'==0
			assert `tax2003start'==0
			local line1=(`tax2004end'-`tax2004start')/`divisor'*250000
			local days2005=td(`tax2005end')-td(`tax2005start')
			local days2006=td(`tax2006end')-td(`tax2006start')
			local line2= (`days2005'+`days2006')/`divisor'*300000
			local line3=400000
				if td(`taxYrEnd')<td(1jan2006) {
				assert `days2006'==0
				local line2=`days2005'/`divisor'*300000
				local line3=0
				}
			local businessLim=`line1'+`line2'+`line3'
			local maxBusinessLimit=`line1'+`line2'+`line3'
			//avoid memory issues
		}
		if `divisor'<357 {
			local businessLim=`line5071'*`divisor'/365
		}
		
		local totalbusinessLim=`businessLim'
		local totalMaxLim=`maxBusinessLimit'
		local totalpaidUp=max(0,`paidUp'-25000000)
		
		if `associated'==1{
			local line5020=`taxable'+`assocTaxable'
			local totalMaxLim'=`maxBusinessLimit'+`assocMaxBusiness'
			local totalbusinessLim=`businessLim'+`assocBusinessLim'
			local totalpaidUp=max(0,`paidUp'+`assocpaidUp'-25000000)
		//above is for CCPC	
		}
	
	local line5069=`totalbusinessLim'-(`totalbusinessLim'*`totalpaidUp'/25000000)
	local line5071=(6000000-10*max(400000,`line5020'))*`line5069'/`totalMaxLim'
	local expLim=min(2000000,`line5071')
	
	local exp=`capitalEx'+`currentEx'
	local line5210=0
	if `exp'<=`expLim' {
		local line5210=`currentEx'+`capitalEx'*0.40
	
	}
	//the other case is very subjective 
	local OITC=`line5210'*0.10
	
	}
	
	if td(`taxYrStart')>=td(1jan2009) {
		local exp=`currentEx'+`capitalEx'*0.40
		
		local entryF=`equipmentRe'*0.25
		local entryG=`entryF'*0.40+`capitalRe'
		local eligibleRepayements=`currentRe'+`entryG'
		
		local variable=`taxableIncome'
		local maxConstraint=400000
		local subtract=7000000
		if `associated'==1 {
			local variable=`taxableIncomeAssoc'
		}
		if td(`taxYrStart')>=(1jan2010) {
			local maxConstraint=500000
			local subtract=8000000
		}
		
		local amount=max(`maxConstraint',`variable')*10
		local excess=max(0,`amount'-`subtract')
		local specifiedCap=max(0,`specifiedCapital'-25000000)
		local line410=max(0, 25000000-`specifiedCap')
		local expLim=`excess'*`line410'/25000000
		if local expLim>3000000 {
			local expLim=3000000
		}
		
		local days=td(`taxYrEnd')-td(`taxYrStart')
		if `days'<357 {
			local expLim=`expLim'*`divisor'/365
		}
		//assuming red expLim refers to one calculated in line 113
		
		local amountCC=`exp'+`eligibleRepayements'
		local amountEE=min(`amountCC,`expLim')
		local OITC=`amountEE'*0.10
		
		if td(`taxYrEnd')>=td(31may2016) {
			local numerator1=td(1june2016)-td(`taxYrStart')
			//including may 31
			local percentage1=`numerator1'/`days'*0.10
			local numerator2=td(`taxYrEnd')-td(1june2016)
			//after may 31
			local percentage2=`numerator2'/`days'*0.08
			local percentage3=`percentage1'+`percentage2'
			local amountS=`eligibleRepayements'*0.10/`percentage3'
			local amountT=`amountS'+`exp'
			local amountp=min(`amountT',`expLim')
			local OITC=`amountp'*`percentage3'
			local amountY=0
			if td(`taxYrStart')>td(31may2016) {
				local amountS=`eligibleRepayementsAfter'*`percentage3'/0.08
				local amountY=`eligibleRepayementsBefore'*1.25	
			}
			local amountZ=`exp'+`amountS'+`eligibleRepaymentYears'+`amountY'
			local OITC=min(`amountZ',`expLim')*.08	
		}
	}
	return scalar OITC=`OITC'
end
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

			
			
			
		