Introduction



This script converts Excel data into an XML file compatible with Tally Prime import.

It supports any number of ledger–amount pairs and applies automatic Debit / Credit logic based on amount values.



Negative amount → Debit (Dr)



Positive amount → Credit (Cr)



The script is intended for structured, digital accounting data (Excel files).





How to use 

Step 1

Open Tally_voucher_template_10_ledgers.xlsx 

Enter your. Use the data example entry mention in the file for reference

For Dr. ledger write ledger name under LEDGER NAME - i and amount needed to be dr. under AMOUNT - i make sure to add (-) in front of amount (example: -100) use "=-" formula in excel to add the minus sigh like show in example 

LEDGER NAME - 1	AMOUNT - 1
purchase	-423.73
 
For Cr. ledger write ledger name under LEDGER NAME - i and amount needed to be dr. under AMOUNT - i make sure to add (+) in front of amount (example: 100) like show in 
example 

LEDGER NAME - 2	AMOUNT - 2
bank a/c	1000.00


Ensure total Debit (Dr) = total Credit (Cr), 
To check you can all the amounts in a row its total should be 0)

Step 2

Open excel_to_Tally.py (make sure all the Requirements are fulfilled before Opening it)

Copy and paste (Tally_voucher_template_10_ledgers.xlsx) file path inside the window (example for file path E:\MULTY LEDGUER ENTRY\Tally_voucher_template_10_ledgers.xlsx)

Press Enter 


Step 3 

it will create the .xml file named Tally_import.xml 

Open the file use ctrl + A and ctrl + c to Copy the content for the file

now Open file name xml format.xml


paste the content in between <REQUESTDATA> and </REQUESTDATA> {Warning don't overwrite xml format.xml}

<REQUESTDATA>

   <!-- Paste content here -->

</REQUESTDATA>

save as the file rename it whatever you like (example my_import.xml) --> make sure to add (.xml) in the end 



Step 4

Open TallyPrime 
on top bar you will see the option to import (short key alt + o)
the go to import --> Transaction 

under File Format xml(Data Interchange)

under File path paste the path of new .xml you have created example my_import.xml (you can access the path by right clicking  example my_import.xml Properties --> Security Object name: file path like E:\Project\my_import.xml

backup yes select backup path and enter it will start importing {Always back up Tally data before importing to avoid issues from incorrect entries.} 










Requirements



A) Dependencies

    1. pandas

    2. Openpyxl



to install use `pip install Openpyxl pandas` after installing python



B) python 3.12 or higher





Note Warning



1\. avoid decimal places higher than 2 (example 103.21 is ok but ***don't use value*** like this ***103.25554***) it will throw an error after importing



2\. make use debit(Dr.) and credit(Cr.) total are same (example 100 Dr. and 100 Cr.)



3\. make sure ledger name you are using have same spelling in TallyPrime if not it will ask you to create new ledger to pass entry


4\. always back up of data before importing