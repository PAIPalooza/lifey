# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take the security of our software seriously. If you discover a security vulnerability, we appreciate your help in disclosing it to us in a responsible manner.

### Reporting Process

1. **Do not** create a public GitHub issue for security vulnerabilities.
2. Email your findings to [SECURITY_EMAIL] with a detailed description of the vulnerability.
3. Include steps to reproduce the issue, if possible.
4. We will acknowledge receipt of your report within 48 hours.
5. We will work on a fix and keep you updated on our progress.
6. Once the issue is resolved, we will release a security update and acknowledge your contribution (unless you prefer to remain anonymous).

### Scope

This security policy applies to all versions of the ALO Backend. When reporting a vulnerability, please specify which version(s) are affected.

### Out of Scope

- Reports that involve social engineering or physical security issues
- Reports from automated tools without proof of concept
- Reports about theoretical vulnerabilities without evidence of exploitability
- Reports about security issues in third-party dependencies (please report them directly to the respective projects)

### Safe Harbor

We consider security research conducted in accordance with this policy to be:
- Authorized in view of any applicable anti-hacking laws, and
- Exempt from restrictions in our Terms of Service.

We will not initiate legal action against security researchers who:
- Engage in testing of systems/research without harming the ALO Backend or its users,
- Engage in vulnerability testing within the scope of this policy,
- Test on products without affecting users, or receive permission/consent from users before engaging in vulnerability testing against their devices.
- Adhere to the laws of their location and the location of the ALO Backend. For example, agreeing to the terms of this policy does not provide authorization to circumvent the Computer Fraud and Abuse Act of 1986.

## Security Best Practices

### For Users

- Always keep your dependencies up to date
- Use strong, unique passwords for all accounts
- Enable two-factor authentication where available
- Regularly review access logs and account activity
- Follow the principle of least privilege when assigning permissions

### For Developers

- Follow secure coding practices
- Keep all dependencies up to date
- Use prepared statements to prevent SQL injection
- Validate and sanitize all user inputs
- Implement proper authentication and authorization checks
- Use HTTPS for all communications
- Implement rate limiting and other security headers
- Regularly audit and update security configurations

## Security Updates

Security updates will be released as patches for the latest minor version. We recommend always running the latest patch version to ensure you have all security fixes.

## Credits

We would like to thank the following individuals and organizations for responsibly disclosing security issues:

- [Your name here]
