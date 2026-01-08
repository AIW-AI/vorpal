# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Vorpal, please report it responsibly.

### How to Report

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email security@vorpal.dev with:

1. **Description**: A clear description of the vulnerability
2. **Impact**: What an attacker could potentially do
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Affected Versions**: Which versions are affected
5. **Suggested Fix**: If you have one (optional)

### What to Expect

- **Acknowledgment**: We will acknowledge your report within 48 hours
- **Assessment**: We will assess the vulnerability and determine severity
- **Updates**: We will keep you informed of our progress
- **Resolution**: We aim to resolve critical issues within 7 days
- **Credit**: We will credit you in the security advisory (unless you prefer otherwise)

### Severity Levels

| Level | Response Time | Examples |
|-------|---------------|----------|
| Critical | 24-48 hours | RCE, auth bypass, data exfiltration |
| High | 7 days | Privilege escalation, PII exposure |
| Medium | 30 days | DoS, information disclosure |
| Low | 90 days | Minor information leaks |

## Security Best Practices

When deploying Vorpal in production:

### Authentication & Authorization

- Always use TLS 1.3 for all connections
- Rotate API keys regularly
- Use short-lived JWT tokens (< 1 hour)
- Enable mTLS for service-to-service communication
- Apply principle of least privilege for RBAC roles

### Database Security

- Use strong passwords for PostgreSQL
- Enable SSL for database connections
- Restrict database network access
- Enable audit logging
- Regular backups with encryption at rest

### Secrets Management

- Never commit secrets to version control
- Use external secrets management (Vault, AWS Secrets Manager, etc.)
- Rotate secrets periodically
- Use separate secrets per environment

### Network Security

- Deploy behind a reverse proxy (nginx, Traefik)
- Enable rate limiting at the gateway level
- Use network policies in Kubernetes
- Restrict egress to necessary destinations only
- Enable DDoS protection for public endpoints

### Monitoring & Auditing

- Enable comprehensive audit logging
- Monitor for anomalous patterns
- Set up alerts for security events
- Regularly review audit logs
- Retain logs per compliance requirements

### Container Security

- Use minimal base images (Alpine)
- Run as non-root user
- Scan images for vulnerabilities
- Sign and verify container images
- Keep base images updated

## Security Features in Vorpal

### vorpal-core

- **Hash-chained audit logs**: Tamper-evident event logging
- **RBAC**: Role-based access control for all operations
- **API key scoping**: Limit keys to specific operations

### vorpal-gateway

- **DLP**: Detect and redact sensitive data (PII, credentials)
- **Prompt injection detection**: Block malicious prompts
- **Rate limiting**: Prevent abuse and DoS

### vorpal-sentinel

- **Autonomy levels**: Restrict agent capabilities
- **Kill switch**: Emergency stop capability
- **HITL**: Human approval for sensitive operations

### vorpal-arbiter

- **Tool permissions**: Fine-grained MCP tool access control
- **Parameter validation**: Prevent injection attacks
- **Budget controls**: Prevent runaway costs

## Compliance

Vorpal is designed to help with compliance for:

- EU AI Act
- NYC Local Law 144
- Colorado SB 205
- NIST AI RMF
- GDPR (data protection aspects)

However, using Vorpal alone does not guarantee compliance. Organizations must implement appropriate policies, procedures, and controls.

## Security Updates

Security updates are released as:

1. **Patch releases**: For vulnerabilities (e.g., 1.0.1)
2. **Security advisories**: Published on GitHub
3. **Announcements**: Posted to our security mailing list

Subscribe to security updates:
- Watch the repository for security advisories
- Join the security mailing list at security-announce@vorpal.dev

## Acknowledgments

We thank the following individuals for responsibly disclosing security issues:

*No reports yet - be the first!*
