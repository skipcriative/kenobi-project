# kenobi/persistence/entities/__init__.py

# Importa todas as entidades para que o SQLAlchemy registre no metadata
from kenobi.persistence.entities.email_log_entity import EmailLog
from kenobi.persistence.entities.audit_event_entity import AuditEvent
from kenobi.persistence.entities.email_recipient_entity import EmailRecipient

# Deixe o arquivo carregar as entidades explicitamente
__all__ = ["EmailLog", "AuditEvent", "EmailRecipient"]
