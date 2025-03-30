
    
import random
import string

def generate_voucher(student_name, correct_answers):
    """Generate a voucher code based on the number of correct answers"""
    
    if correct_answers <= 2:
        voucher_name = "You are not eligible for any offer"
    elif correct_answers <= 3:
        voucher_name = "Silver"
    elif correct_answers <= 4:
        voucher_name = "Gold"
    else:
        voucher_name = "Platinum"
    
    # Generate a random alphanumeric string for the voucher
    voucher_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    
    # Return the full voucher string
    return f"{voucher_name}-{voucher_code}"
    
    
    
    