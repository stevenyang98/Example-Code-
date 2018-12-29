//27 June 2018
//Quebec

program form1
	args endDate beginDate partnership ccpc associated associatedExpLimit box63or64 box5Aor5B amountH line171Copy interposedPartner qualifiedPartner assistanceRecieved
	assitanceRepaid amountHorK line462
	subcontractor armslength  salaryPaid considerationPaid contributions assistanceRelated assets universityResearch feesConsortorium qualifiedPreComp
	
	//for now we ignore type of qualified tax payer
	//ignore subcontractors for now
	//all seperate 
	//asks for dates of the R&D contract beginning, ignore this distinction for now
	//ask Ian for how the subcontractor works/will write the code for it later
	local line130=`salaryPaid'+`considerationPaid'
	local line132=`line130'-`contributions'
	local line149=`line132'-`assistanceRelated'
	local line152a=0
	
	//if the tax year begins after 3dec2014, we do part 4 of the form
	local taxCredit=0
	//placeholder
	
	if td(`beginDate')>(3dec2014) {
		local line156h=0 
		if `assets'<=50000000 {
			local line156h=50000
		}
		if `assets'>=75000000 {
			local line156h=75000
		}
			//form says to do this if assets have these values. Up next, third case where it is in between
		if `assets'>50000000 & if `assets'<75000000 {
			//now we have to do some calculations
			local line156c=`assets'-50000000
			local line156e=`line156c'/25000000
			local line156g=`line156e'*175000
			local line156h=`line156g'+50000
			//simply following form directions
		}
		//now we have line156h values for all three cases, so now we do some calculations with this values
		local line156i=td(`endDate')-td(`beginDate')
		//line 156i is number of days in tax year
		local line156k=`line156i'/365
		local line157=`line156h'*`line156k'
		//this is the exclusion threshold, not sure what it is but this is how you calculate it
		//for the next set of calculations, you cannot include expenditures after 2dec2014
		local line158=`line130'
		//the next line relies on something obtained by doing another form, but we can request to chester that in the data this is a given
		//RD-1029.8.16.1-V this is the form 
		local line162=`line158'+`universityResearch'+`feesConsortorium'+`qualifiedPreComp'
		//injecting the other forms
		local line163=min(`line162',`line157')
		if line163==`line157' {
			local taxCredit=0
			//s. If the amount on line 162 is less than the amount on line 157, the taxpayer cannot claim the tax credit for the taxation year
		}
		local line167=`line163'*`line158'/`line162'
		local line152a=`line167'
	}
	local line152b=`line149'-`line152a'
	//applicable percentage will change, depending on type of subcontractor
	local line154=`line152b'
	local line155=`line154'
	//doesn't account for subcontractors yet
	if `line154'<0{
		local line155=0
		//qualified expenditures
	}
	
	/* Complete Part 5 only if the taxpayer is a Canadian-controlled corporation whose assets (including those of any corporations associated with it) are less than
	$75 million for the previous taxation year. In other cases, go to Part 7 */
	// RD-1029.7.8,  determines expenditure for associated, ask chester for this number
	if `ccpc'==1 & if `assets'>75000000 {
		local line168==3000000
		if `associated'==1 {
			local line168=`associatedExpLimit'
		}
		local line170=`line168'*`line156k'
		//not related, but it says multiply line168 by number tax days/365, which we computed in line 156k
		local line170b=`line170'-`line152a'
		//might have to change this once we account for subcontractors, but this works for now
		local line171=0
		if `box63or64'==63 {
			local line171= min(`amountH',`line170b')
			//not sure what amountH is, Cora can you look into this?
		}
		local line176=0
		local line175=0
		if `box63or64'==64 {
			local line175=`line170b'-`line171Copy'
			//If the taxation year concerned includes June 4, 2014 I don't think we need to make a boolean tree here because the firm should know this
			local line176=min(`amountH',`line175')
		} 
	}
	
	//stopped at Part 5, going home now, will do later tomorrow 
	if `partnership'==1 {
		local line207=`interposedPartner'*`qualifiedPartner'
		//from my understanding this is something the coorporation knows and they simply input it into the form
		
		//program does not look at RL-15 slip, can look at it later if we need to. Make line 71-1 and 71-2 inputs for now
		local line208c=`line149'*`line207'
		//make seperate arguments for each one
		local line208e=`line208c'-`assistanceRecieved'
		local line208f=0
		if td(`beginDate')<td(3dec2014) {
			local line208f=`line167'
			//if year begins before 3dec2014 use quantity determined in line167
		}
		local line208h=`line208f'*`line207'
		local line209=`line208e'-`line208h'
		local line209b=`line209'
		//similar to above, applicable percentage changes, but need someone to explain what it actually means
		local line210=max(`line209b',0)
		//qualified expenditures
	}
	
	
	local line241=`amountHorK'
	//company should know which applies
	local line244=0.175
	if `box63or64'==64 {
		local line244=0.14
	}
	local line244a=`line241'*`line244'
	local line245=`line244a'+`assistanceRelated'+`line462'
	//line462 is from another form
	local taxCredit=`line245'
		
	
	if `corporation'==1 {
		//if you are a corporation, tax credit is calculated differently
		//might be CCPC
		//H or K reference line numbers
		local line212=.375
		if `box63or64'==64 {
			local line212=.3
		}
		local line215=max(`assets'-50000000,0)
		local applicableRate=0
		//four scenarios that determine this rate
		if `box5Aor5B'==5A | if `box63or64'==63 {
			local applicableRate=0.20
		}
		if `box5Aor5B'==5A | if `box63or64'==64 {
			local applicableRate=0.16
		}
		if `box5Aor5B'==5B | if `box63or64'==63 {
			local applicableRate=0.10
		}
		if `box5Aor5B'==5B | if `box63or64'==64 {
			local applicableRate=0.08
		}
		//would be cool to see why the rates must change
		local line217=`line215'*`applicableRate'
		local line219=`line217'/250000
		//should be in units of percentage
		local line220=`line212'-`line219'
		//increased tax credit rate is line220
		local line225=`line176'
		//or line 171, whichever is applicable. Not sure what this means
		local line227=`line225'*`line220'
		local line230=max(0,`amountH'-`line225')
		local line231=0
		if `box5Aor5B'==5A | if `box63or64'==63 {
			local line231=0.175
		}
		if `box5Aor5B'==5A | if `box63or64'==64 {
			local line231=0.14
		}
		if `box5Aor5B'==5B | if `box63or64'==63 {
			local line231=0.275
		}
		if `box5Aor5B'==5B | if `box63or64'==64 {
			local line231=0.22
		}
		local line232=`line230'*`line231'
		local line235=`line227'+`line232'+`assitanceRepaid'
		//not sure if these are different assistances or not
		local taxCredit=`line235'	
	}
	return scalar TaxCredit=`taxCredit'
	
	//print out and revise it, deep read it 
	
	