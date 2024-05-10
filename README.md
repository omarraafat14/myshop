# MyShop
- A fully-featured online shop built with Django that implements essential e-commerce functionalities.
- Customers can browse products, add them to carts, apply discounts, checkout securely, and receive invoices.
- A recommendation engine suggests relevant products, and internationalization enables multi-language support


## Technical Features

### Product Management:
- Create and manage a comprehensive product catalog with rich details.
### Shopping Cart:
- Utilize Django sessions for a seamless shopping cart experience.
- Implement a custom context processor for convenient cart access across views.
### Order Management:
- Allow customers to finalize purchases and track order history.
- Asynchronous Tasks with Celery and RabbitMQ:
- Configure Celery for background tasks like sending notifications.
- Leverage RabbitMQ as a message broker for efficient task management.
### Customer Notifications:
- Send automated email or SMS notifications to customers about orders, discounts, etc. (Integration with a notification service would be needed)
### Monitoring with Flower:
- Monitor Celery task execution and performance using Flower's web interface.
### Secure Payments with Stripe:
- Integrate the Stripe payment gateway for secure credit card processing.
- Handle payment notifications for seamless transaction confirmation.
### Order Reporting:
- Export orders to CSV files for easy data analysis and management.
### Administration Panel:
- Create custom views for a user-friendly admin interface.
### Dynamic PDF Invoices:
- Generate PDF invoices with essential order details.
### Coupon System:
- Create and manage coupons for discounts.
- Apply coupons to shopping carts and orders for flexible promotions.
- Support coupon creation for Stripe Checkout (if needed)
### Product Recommendations:
- Build a product recommendation engine with Redis to enhance customer engagement.




## Installation


1. Prerequisites
   - Python (https://www.python.org/downloads/)
   - RabbitMQ (https://www.rabbitmq.com/)
   - Celery (https://docs.celeryq.dev/)
   - Flower (https://flower.readthedocs.io/)
   - Stripe account (https://stripe.com/) (for payment processing)

2. Clone Repository:
   - `git clone https://github.com/omarraafat14/myshop.git`



3. Set Up Environment:
   ~~~
   cd myshop
   source env/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   ~~~
- Note: Create a .env file to store sensitive information like Stripe API keys and database credentials (refer to Django documentation for details).


4. Run RabbitMQ:
   - (Optional for asynchronous tasks with Celery)
   ~~~
   docker pull rabbitmq
   docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
   ~~~

5. Start Celery Worker:
   - `celery -A <project-name> worker -l info`


6. Monitor Celery (optional):
   - `celery -A myshop flower`
   - This opens Flower's web interface (usually at http://localhost:5555) for monitoring Celery tasks.



## Usage

1. Start the Django development server:
   - `python manage.py runserver`

2. Explore the app's functionalities using the admin panel and frontend.
