import xmlrpclib
import datetime

username = 'admin' 
password = 'admin'      
dbname = 'student'    

sock_common = xmlrpclib.ServerProxy ('http://localhost:8073/xmlrpc/common')
uid = sock_common.login(dbname, username, password)

sock = xmlrpclib.ServerProxy('http://localhost:8073/xmlrpc/object')

check_account_id = sock.execute_kw(dbname, uid, password,'res.partner', 'search_read',[[('customer', '=', True)]],{'limit': 1, 'fields': ['property_account_receivable_id',]})[0]


check_tax = [('name', '=', 'Tax 8.00%'), ('type_tax_use', '=', 'sale')]
tax_ids = sock.execute(dbname, uid, password, 'account.tax', 'search', check_tax)
print(tax_ids)

check_tags = [('name', '=', 'Employee')]
tag_ids = sock.execute(dbname, uid, password, 'res.partner.category', 'search', check_tags)[0]
print(tag_ids)
partnar_tags = [(4,tag_ids)]

check_partner_id = [('name', '=', 'Tom cruse')]
check_partner_ids = sock.execute(dbname, uid, password, 'res.partner', 'search', check_partner_id)[0]
print(check_partner_ids)

update_vals_partner = {'category_id' : partnar_tags}
print(update_vals_partner)
update_partner_tag = sock.execute(dbname, uid, password, 'res.partner', 'write' ,check_partner_ids, update_vals_partner)
print(update_partner_tag)
	
invoice_line_tax = [[6,0,tax_ids]]

create_invoice_lines = []

create_invoice_line = [{
			'name': 'Product desc',
        	'account_id': check_account_id['property_account_receivable_id'][0],
        	'price_unit':15.0,
        	'invoice_line_tax_ids':invoice_line_tax,
        	},{
        	'name': 'Ice shh desc',
        	'account_id': check_account_id['property_account_receivable_id'][0],
        	'price_unit':50.0,
        	'invoice_line_tax_ids':invoice_line_tax,
        	}]

for i in create_invoice_line:
	create_invoice_lines.append((0,0,i))

create_new_partner = {
   'name': 'Tom cruse',
   'email': 'tom@test.com',
   'company_type' : 'person',
   'street': 'Alex street 40',
   'street2': 'chakli circle street',
   'zip': '1367',
   'city': 'Grand-Rosiere',
   'phone': '+55555',
   'mobile':'9660138737',
   'state_id' : 'Gujarat',
   'country_id': 'India',
}

state = False
if create_new_partner and create_new_partner.get('state_id'):
   state = create_new_partner.get('state_id')

country = False
if create_new_partner and create_new_partner.get('country_id'):
   country = create_new_partner.get('country_id')

check_state = [('name', '=', state)] 
state_id = sock.execute(dbname, uid, password, 'res.country.state', 'search', check_state)

check_country = [('name', '=', country)]
country_id = sock.execute(dbname, uid, password, 'res.country', 'search', check_country)

email = False
if create_new_partner and create_new_partner.get('email'):
   email_id = create_new_partner.get('email')
  
check_email = [('email', '=', email_id)] 
email_updated_id = sock.execute(dbname, uid, password, 'res.partner', 'search', check_email)
   
partner_vals = {
   'name': create_new_partner and create_new_partner.get('name'),
   'email': create_new_partner and create_new_partner.get('email'),
   'company_type' : create_new_partner and create_new_partner.get('company_type'),
   'street': create_new_partner and create_new_partner.get('street'),
   'street2': create_new_partner and create_new_partner.get('street2'),
   'zip': create_new_partner and create_new_partner.get('zip'),
   'city': create_new_partner and create_new_partner.get('city'),
   'phone': create_new_partner and create_new_partner.get('phone'),
   'mobile':create_new_partner and create_new_partner.get('mobile'),
   'state_id': state_id[0],
   'country_id': country_id[0],
}

partner_with_email = {
   'name': create_new_partner and create_new_partner.get('name'),
   'company_type' : create_new_partner and create_new_partner.get('company_type'),
   'street': create_new_partner and create_new_partner.get('street'),
   'street2': create_new_partner and create_new_partner.get('street2'),
   'zip': create_new_partner and create_new_partner.get('zip'),
   'city': create_new_partner and create_new_partner.get('city'),
   'phone': create_new_partner and create_new_partner.get('phone'),
   'mobile':create_new_partner and create_new_partner.get('mobile'),
   'state_id': state_id[0],
   'country_id': country_id[0],
}

if email_updated_id:
	partner_id = sock.execute(dbname, uid, password, 'res.partner', 'write', email_updated_id ,partner_with_email)
	print(partner_id)
else:	
	partner_id = sock.execute(dbname, uid, password, 'res.partner', 'create', partner_vals)
	print(partner_id)

res_partner_name = create_new_partner.get('name')
date_today = datetime.date.today()
now_date = date_today.strftime('%Y-%m-%d')

vals_master = {
			'partner_name' : [('name','=', res_partner_name)],
			'payment_term_name': [('name', '=', 'Immediate Payment')],
			'date_of_invoice': now_date,
			# 'date_of_invoice': '2019-11-17',
			}

create_partner = sock.execute(dbname, uid, password, 'res.partner', 'search', vals_master['partner_name'])[0]
create_payment_term = sock.execute(dbname, uid, password, 'account.payment.term', 'search', vals_master['payment_term_name'])[0]
vals_master_date_invoice = vals_master['date_of_invoice']

partner = {
		'partner_id': create_partner,
		'payment_term_id': create_payment_term,
		'date_invoice': vals_master_date_invoice,
    'invoice_line_ids': create_invoice_lines,
        }
print(partner)

############create record########

create_partner_ids = sock.execute(dbname, uid, password, 'account.invoice', 'create', partner)
print(create_partner_ids)



