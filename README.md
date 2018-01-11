usage: ApiWordlistGen.py [-h] [--format FORMAT] [--out OUT] formula  

Generate wordlists for API fuzzing from basic wordlists  

positional arguments:  
  formula               # ApiWordlistGen support schemes in format "vpnfbni,vn,vnBbI", where:  
                        v - word from verb wordlist  
                        p - word from prefix wordlist  
                        n - word from noun wordlist  
                        N - word from noun wordlist extend by plural form ("*ss"->"*sses", "*y"->"*ies", "*x"-> "*xes", default just add "s")  
                        f - word from postfix wordlist  
                        B - word "By"  
                        b - word from by wordlist  
                        I - word "Id"  

optional arguments:
  -h, --help            show this help message and exit
  --format FORMAT, -f FORMAT
                        Define style of generated words.
                        Possible values:
                        camel -> GetCustomerNameById
                        lower_chain -> get_customer_name_by_id
                        camel_chain -> Get_Customer_Name_By_Id
                        upper_chain -> GET_CUSTOMER_NAME_BY_ID
  --out OUT, -o OUT     Name of generated file

ApiWordlistGen generates wordlist that contains concatinations of all word combinations that matches formula. If more than one formula separated by comma are specifed, ApiWordlistGen generate one merged list.
Empty strings exists in postfix in prefix wordlists, So list for formula without "p" or "f" is subset of list for formula with "p" or "f".

Example:
python ApiWordlistGen.py -f camel -o out.txt vpnfbni,vn,vnBbI

