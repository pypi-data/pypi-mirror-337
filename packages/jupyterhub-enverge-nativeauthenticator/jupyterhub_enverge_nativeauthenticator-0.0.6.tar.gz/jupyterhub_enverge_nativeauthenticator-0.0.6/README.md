# Enverge Native Authenticator

> **Sponsored by [Enverge.ai](https://enverge.ai)** - Simpler, greener, cheaper AI training platform. Enverge harnesses excess green energy for powerful, cost-effective computing on GPUs, enabling environmentally friendly AI model development, training, and fine-tuning. Currently in private alpha with limited spots available.

A JupyterHub authenticator that extends the native authenticator with email notifications for user authorization.

## Overview & Features

This package extends [jupyterhub-nativeauthenticator](https://github.com/jupyterhub/nativeauthenticator) with the following enhancements:

- **User Registration & Admin Approval**: Allows users to sign up while requiring admin approval of new accounts
- **Authorization Emails**: Sends notification emails to users when their accounts are approved
- **Email Delivery Management**:
  - Integration with SendGrid for reliable email delivery
  - Tracking of email delivery status to prevent duplicate notifications
- **Modern UI**: Customized and improved templates for authentication screens

## Installation

```bash
pip install jupyterhub-enverge-nativeauthenticator
```

Or for development:

```bash
git clone https://github.com/Enverge-Labs/enverge_nativeauthenticator
cd enverge_nativeauthenticator
pip install -e .
```

## Configuration

Add the following to your `jupyterhub_config.py`:

```python
c.JupyterHub.authenticator_class = 'enverge_native'

# Email configuration
c.EnvergeNativeAuthenticator.sendgrid_api_key = 'your-sendgrid-api-key'  
c.EnvergeNativeAuthenticator.email_sender = 'your-sender-email@example.com'
c.EnvergeNativeAuthenticator.sendgrid_template_id_authorization_email = 'your-sendgrid-template-id'

# Optional: All inherited NativeAuthenticator settings are supported
```

### Environment Variables

You can also set these configuration options via environment variables:

- `SENDGRID_API_KEY`: Your SendGrid API key
- `EMAIL_SENDER`: Email address to be shown as the sender

## SendGrid Templates

This authenticator uses SendGrid dynamic templates for email notifications. The templates should include:

- A `name` variable for the username

You can create and manage your email templates in the [SendGrid Dynamic Templates](https://mc.sendgrid.com/dynamic-templates) interface.

## Design Decisions

- **Extending Native Authenticator**: Built on top of the established JupyterHub Native Authenticator to maintain compatibility and leverage its security features.
- **Optional Email Integration**: Email functionality requires SendGrid but remains optional, falling back gracefully if not configured.
- **Database Tracking**: Uses SQLAlchemy ORM to track which users have received authorization emails, avoiding duplicate notifications.
- **Pluggable Authentication**: Follows JupyterHub's authentication plugin system for seamless integration.

## Development

Setup a development environment:

```bash
# Clone the repository
git clone https://github.com/Enverge-Labs/enverge_nativeauthenticator
cd enverge_nativeauthenticator

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[test]"
```

## License

3-Clause BSD License, same as JupyterHub.

