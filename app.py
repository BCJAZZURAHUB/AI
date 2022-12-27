import openai
import paypalrestsdk
import streamlit as st

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY_HERE"

# Set your PayPal API credentials
paypalrestsdk.configure({
  "mode": "sandbox", # Use sandbox mode for testing
  "client_id": "YOUR_CLIENT_ID_HERE",
  "client_secret": "YOUR_CLIENT_SECRET_HERE"
})

# Add a header to the main content area
st.header("BC JAZZURA AI")

# Use the st.sidebar to create a sidebar where users can select their subscription type
subscription_type = st.sidebar.radio("Subscription type", ("Free", "Monthly", "Premium"))

# Use the st.text_area function to create a text area where the user can enter a text description
text_description = st.text_area("Enter a text description")

# Use the openai module's Completion class to create a completion object for the DALL-E model
completion = openai.Completion.create(engine="image-alpha-001", prompt=text_description)

# Use the completion object's complete method to generate an image from the text description
image = completion.complete(prompt=text_description)

# Use the st.image function to display the image
st.image(image)

# Use the openai module's Completion class to create a completion object for the BART model
bart = openai.Completion.create(engine="davinci", prompt=text_description)

# Use the bart object's complete method to generate text from the text description
generated_text = bart.complete(prompt=text_description)

# Use the st.write function to display the generated text
st.write(generated_text)

# Use the st.text_input function to create a text input field where the user can enter a message
message = st.text_input("Enter a message")

# Use the openai module's Completion class to create a completion object for the GPT-3 model
gpt3 = openai.Completion.create(engine="text-davinci-002", prompt=message)

# Use the gpt3 object's complete method to generate a response to the message
response = gpt3.complete(prompt=message)

# Use the st.write function to display the response
st.write(response)

# Check the subscription type of the user
if subscription_type == "Free":
    # If the user is a free user, allow them to send 5 messages per day
    messages_remaining = st.sidebar.slider("Messages remaining", min_value=0, max_value=5, value=5)
    if messages_remaining > 0:
        # Deduct one message when the user sends a message
        messages_remaining -= 1
        st.write("Your message has been sent.")
    else:
        st.write("You have exceeded the maximum number of messages for free users.")
elif subscription_type == "Monthly":
    # If the user is a monthly subscriber, allow them to send 50 messages per day
    messages_remaining = st.sidebar.slider("Messages remaining", min_value=0, max_value=50, value=50)
    if messages_remaining > 0:
        # Deduct one message when the user sends a message
        messages_remaining -= 1
        st.write("Your message has been sent.")
    else:
        st.write("You have exceeded the maximum number of messages for monthly subscribers.")
elif subscription_type == "Premium":
    # If the user is a premium subscriber, allow them to send unlimited messages
    st.write("Your message has been sent.")

# Use the st.sidebar function to create a button that allows users to pay for a subscription
if st.sidebar.button("Subscribe now"):
    # Create a payment object
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8501/subscribe/success",
            "cancel_url": "http://localhost:8501/subscribe/cancel"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": subscription_type,
                    "sku": subscription_type,
                    "price": "20.00" if subscription_type == "Monthly" else "30.00",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "20.00" if subscription_type == "Monthly" else "30.00",
                "currency": "USD"
            },
            "description": f"{subscription_type} subscription to BC JAZZURA AI"
        }]
    })

    # Create the payment
    if payment.create():
        # If the payment was created successfully, loop through the payment links to find the approval URL
        for link in payment.links:
            if link.method == "REDIRECT":
                # Redirect the user to the approval URL
                redirect_url = link.href
                st.markdown(f'<a href="{redirect_url}" target="_blank">Click here to approve the payment</a>',
                            unsafe_allow_html=True)
        else:
            # If the payment was not created successfully, display an error message
            st.write("An error occurred while creating the payment:")
            st.write(payment.error)

    # Use the st.sidebar function to create a button that allows users to cancel their subscription
    if st.sidebar.button("Cancel subscription"):
        # Use the st.text_input function to create a text input field where the user can enter their subscription ID
        subscription_id = st.text_input("Enter your subscription ID")

        # Use the paypalrestsdk module's Subscription class to create a subscription object
        subscription = paypalrestsdk.Subscription.find(subscription_id)

        # Use the subscription object's cancel method to cancel the subscription
        if subscription.cancel():
            st.write("Your subscription has been cancelled.")
        else:
            st.write("An error occurred while cancelling your subscription:")
            st.write(subscription.error)



