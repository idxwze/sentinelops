from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

import gradio as gr
import plotly.graph_objects as go
from plotly.subplots import make_subplots


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


TEXT = {
    "en": {
        "tagline": "AI incident copilot for reliability and security triage",
        "subtitle": "Review live signals, isolate likely causes, and decide the next safe action faster.",
        "workspace_status": "Workspace status",
        "language": "Language",
        "text_size": "Text size",
        "contrast": "High contrast",
        "compact": "Compact",
        "comfortable": "Comfortable",
        "large": "Large",
        "nav_dashboard": "Dashboard",
        "nav_incidents": "Incidents",
        "nav_copilot": "Copilot",
        "nav_profile": "Profile",
        "queue_title": "Incident queue",
        "queue_subtitle": "Active incidents and current response state",
        "incident_selector": "Selected incident",
        "summary_title": "Incident summary",
        "summary_subtitle": "Current condition and recent operational context",
        "signals": "Core signals",
        "signals_subtitle": "Latency and error behavior for the selected service",
        "load": "Infrastructure and traffic",
        "load_subtitle": "Capacity pressure and request shape",
        "dependencies": "Service dependencies",
        "dependencies_subtitle": "Connected systems affected by this incident",
        "hypotheses": "Ranked hypotheses",
        "hypotheses_subtitle": "Most likely explanations based on current evidence",
        "actions": "Recommended actions",
        "actions_subtitle": "Practical next checks for the on-call engineer",
        "profile_title": "Analyst profile",
        "profile_subtitle": "Local prototype profile and working preferences",
        "profile_name": "Name",
        "profile_role": "Role",
        "profile_team": "Team",
        "profile_language": "Preferred language",
        "profile_focus": "Alert focus",
        "profile_status": "On-call status",
        "profile_name_value": "Maya Chen",
        "profile_role_value": "Junior SRE",
        "profile_team_value": "Platform Reliability",
        "profile_focus_value": "Payments and authentication",
        "profile_status_value": "Primary on-call",
        "copilot": "AI copilot",
        "copilot_subtitle": "Incident-aware assistant for triage and explanation",
        "copilot_placeholder": "Ask about likely cause, blast radius, recent changes, or the best next check...",
        "copilot_empty": "Choose an incident to start a focused triage conversation.",
        "copilot_closed": "Copilot minimized",
        "copilot_open": "Copilot ready",
        "launcher": "Open Copilot",
        "close_chat": "Close",
        "suggested_prompts": "Suggested prompts",
        "ask_button": "Send",
        "why_checkout": "Why is checkout failing?",
        "recent_changes": "What changed recently?",
        "root_cause": "What is the most likely root cause?",
        "check_first": "What should I check first?",
        "security_concern": "Is there a security concern?",
        "current_state": "Current state",
        "recent_change": "Recent change",
        "affected_service": "Affected service",
        "latency": "Latency",
        "error_rate": "Error rate",
        "cpu": "CPU",
        "requests": "Request volume",
        "confidence": "Confidence",
        "next_check": "Next check",
        "footer_note": "SentinelOps prototype for incident triage and reliability UX",
        "status_loading": "Loading incident context",
        "status_loaded": "Incident context loaded",
        "status_no_incident": "Select an incident to unlock the workspace",
        "status_chat_blocked": "Select an incident before using the copilot",
        "status_no_question": "Enter a question or choose a prompt",
        "assistant_intro": "Copilot ready. I can summarize likely causes, recent changes, dependency impact, and recommended next checks.",
        "empty_hypotheses": "No hypotheses are available for this incident yet.",
        "empty_dependencies": "No dependency impact data available.",
        "empty_overview": "Select an incident from the queue to inspect service health, signals, and likely causes.",
        "unavailable": "Unavailable",
    },
    "fr": {
        "tagline": "Copilote IA d'incident pour le triage fiabilite et securite",
        "subtitle": "Analysez les signaux, isolez les causes probables et choisissez plus vite la prochaine action sure.",
        "workspace_status": "Etat de l'espace",
        "language": "Langue",
        "text_size": "Taille du texte",
        "contrast": "Contraste eleve",
        "compact": "Compact",
        "comfortable": "Confortable",
        "large": "Grand",
        "nav_dashboard": "Tableau",
        "nav_incidents": "Incidents",
        "nav_copilot": "Copilote",
        "nav_profile": "Profil",
        "queue_title": "File d'incidents",
        "queue_subtitle": "Incidents actifs et etat actuel de reponse",
        "incident_selector": "Incident selectionne",
        "summary_title": "Resume de l'incident",
        "summary_subtitle": "Etat actuel et contexte operationnel recent",
        "signals": "Signaux principaux",
        "signals_subtitle": "Comportement de latence et d'erreur pour le service selectionne",
        "load": "Infrastructure et trafic",
        "load_subtitle": "Pression de capacite et forme du trafic",
        "dependencies": "Dependances du service",
        "dependencies_subtitle": "Systemes connectes touches par cet incident",
        "hypotheses": "Hypotheses classees",
        "hypotheses_subtitle": "Explications les plus probables selon les preuves actuelles",
        "actions": "Actions recommandees",
        "actions_subtitle": "Prochains controles concrets pour l'ingenieur d'astreinte",
        "profile_title": "Profil analyste",
        "profile_subtitle": "Profil local du prototype et preferences de travail",
        "profile_name": "Nom",
        "profile_role": "Role",
        "profile_team": "Equipe",
        "profile_language": "Langue preferee",
        "profile_focus": "Focus alertes",
        "profile_status": "Statut d'astreinte",
        "profile_name_value": "Maya Chen",
        "profile_role_value": "SRE junior",
        "profile_team_value": "Fiabilite plateforme",
        "profile_focus_value": "Paiements et authentification",
        "profile_status_value": "Astreinte principale",
        "copilot": "Copilote IA",
        "copilot_subtitle": "Assistant contextuel pour le triage et l'explication",
        "copilot_placeholder": "Posez une question sur la cause probable, la portee, les changements recents ou le meilleur prochain controle...",
        "copilot_empty": "Choisissez un incident pour commencer une conversation de triage ciblee.",
        "copilot_closed": "Copilote reduit",
        "copilot_open": "Copilote pret",
        "launcher": "Ouvrir le copilote",
        "close_chat": "Fermer",
        "suggested_prompts": "Invites suggerees",
        "ask_button": "Envoyer",
        "why_checkout": "Pourquoi le checkout echoue-t-il ?",
        "recent_changes": "Qu'est-ce qui a change recemment ?",
        "root_cause": "Quelle est la cause la plus probable ?",
        "check_first": "Que dois-je verifier en premier ?",
        "security_concern": "Y a-t-il un risque de securite ?",
        "current_state": "Etat actuel",
        "recent_change": "Changement recent",
        "affected_service": "Service affecte",
        "latency": "Latence",
        "error_rate": "Taux d'erreur",
        "cpu": "CPU",
        "requests": "Volume de requetes",
        "confidence": "Confiance",
        "next_check": "Prochain controle",
        "footer_note": "Prototype SentinelOps pour le triage d'incident et l'UX fiabilite",
        "status_loading": "Chargement du contexte d'incident",
        "status_loaded": "Contexte d'incident charge",
        "status_no_incident": "Selectionnez un incident pour activer l'espace de travail",
        "status_chat_blocked": "Selectionnez un incident avant d'utiliser le copilote",
        "status_no_question": "Saisissez une question ou choisissez une invite",
        "assistant_intro": "Copilote pret. Je peux resumer les causes probables, les changements recents, l'impact sur les dependances et les prochains controles recommandes.",
        "empty_hypotheses": "Aucune hypothese n'est disponible pour cet incident.",
        "empty_dependencies": "Aucune information sur l'impact des dependances.",
        "empty_overview": "Selectionnez un incident dans la file pour inspecter la sante du service, les signaux et les causes probables.",
        "unavailable": "Indisponible",
    },
}


SEVERITY_COLORS = {
    "Critical": "#dc2626",
    "High": "#ea580c",
    "Medium": "#ca8a04",
    "Low": "#16a34a",
}

STATUS_COLORS = {
    "Investigating": "#b45309",
    "Mitigating": "#2563eb",
    "Escalated": "#be123c",
    "Monitoring": "#0f766e",
    "Contained": "#7c3aed",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_datasets():
    incidents = load_json(DATA_DIR / "incidents.json")
    metrics = load_json(DATA_DIR / "metrics.json")
    hypotheses = load_json(DATA_DIR / "hypotheses.json")
    return incidents, metrics, hypotheses


INCIDENTS, METRICS, HYPOTHESES = load_datasets()
INCIDENT_MAP = {incident["id"]: incident for incident in INCIDENTS}


def t(lang: str, key: str) -> str:
    return TEXT.get(lang, TEXT["en"]).get(key, key)


def format_number(value: float, unit: str = "") -> str:
    if unit == "%":
        return f"{value:.1f}%"
    if unit == "ms":
        return f"{int(value)} ms"
    if unit == "rpm":
        return f"{int(value):,} rpm"
    return f"{value}"


def get_incident_label(incident: Dict, lang: str) -> str:
    return f"{incident[f'title_{lang}']} | {incident['severity']} | {incident['service']}"


def get_incident_choices(lang: str) -> List[Tuple[str, str]]:
    return [(get_incident_label(incident, lang), incident["id"]) for incident in INCIDENTS]


def get_accessibility_classes(text_size: str, contrast: bool) -> str:
    contrast_class = "contrast-on" if contrast else "contrast-off"
    size_class = f"size-{text_size}"
    return f"{contrast_class} {size_class}"


def build_header_html(lang: str, text_size: str, contrast: bool) -> str:
    classes = get_accessibility_classes(text_size, contrast)
    return f"""
    <div class="topbar-shell {classes}">
        <div class="brand-cluster">
            <div class="brand-mark">SO</div>
            <div class="brand-copy">
                <div class="brand-title">SentinelOps</div>
                <div class="brand-subtitle">{t(lang, 'subtitle')}</div>
            </div>
        </div>
        <div class="nav-cluster">
            <div class="nav-item active">{t(lang, 'nav_dashboard')}</div>
            <div class="nav-item">{t(lang, 'nav_incidents')}</div>
            <div class="nav-item">{t(lang, 'nav_copilot')}</div>
            <div class="nav-item">{t(lang, 'nav_profile')}</div>
        </div>
        <div class="account-cluster">
            <div class="account-meta">
                <div class="account-label">{t(lang, 'workspace_status')}</div>
                <div class="account-value">SentinelOps / MVP</div>
            </div>
            <div class="account-avatar">MC</div>
        </div>
    </div>
    """


def build_status_html(message: str, lang: str, text_size: str, contrast: bool, mode: str = "neutral") -> str:
    classes = get_accessibility_classes(text_size, contrast)
    return f"""
    <div class="status-shell {classes} mode-{mode}">
        <div class="status-label">{t(lang, 'workspace_status')}</div>
        <div class="status-value">{message}</div>
    </div>
    """


def build_section_heading(title: str, subtitle: str) -> str:
    return f"""
    <div class="section-heading">
        <div class="section-title">{title}</div>
        <div class="section-subtitle">{subtitle}</div>
    </div>
    """


def build_footer_html(lang: str) -> str:
    return f"""
    <div class="footer-shell">
        <div class="footer-left">SentinelOps</div>
        <div class="footer-right">{t(lang, 'footer_note')}</div>
    </div>
    """


def build_incident_cards(selected_id: str | None, lang: str, text_size: str, contrast: bool) -> str:
    classes = get_accessibility_classes(text_size, contrast)
    cards = []
    for incident in INCIDENTS:
        selected_class = "selected" if incident["id"] == selected_id else ""
        severity_color = SEVERITY_COLORS.get(incident["severity"], "#64748b")
        status_color = STATUS_COLORS.get(incident["status"], "#64748b")
        cards.append(
            f"""
            <div class="incident-card {classes} {selected_class}">
                <div class="incident-card-top">
                    <span class="severity-pill" style="background:{severity_color};">{incident['severity']}</span>
                    <span class="status-pill" style="color:{status_color}; border-color:{status_color};">{incident['status']}</span>
                </div>
                <div class="incident-title">{incident[f'title_{lang}']}</div>
                <div class="incident-meta">{incident['service']} • {incident['timestamp']}</div>
                <div class="incident-description">{incident[f'short_status_{lang}']}</div>
            </div>
            """
        )
    return "\n".join(cards)


def build_profile_html(lang: str, text_size: str, contrast: bool) -> str:
    classes = get_accessibility_classes(text_size, contrast)
    items = [
        (t(lang, "profile_name"), t(lang, "profile_name_value")),
        (t(lang, "profile_role"), t(lang, "profile_role_value")),
        (t(lang, "profile_team"), t(lang, "profile_team_value")),
        (t(lang, "profile_language"), "EN / FR"),
        (t(lang, "profile_focus"), t(lang, "profile_focus_value")),
        (t(lang, "profile_status"), t(lang, "profile_status_value")),
    ]
    rows = "".join(
        [
            f"""
            <div class="profile-row">
                <div class="profile-key">{label}</div>
                <div class="profile-value">{value}</div>
            </div>
            """
            for label, value in items
        ]
    )
    return f"""
    <div class="panel-card profile-card {classes}">
        <div class="profile-top">
            <div>
                <div class="profile-avatar">MC</div>
            </div>
            <div class="profile-summary">
                <h3>{t(lang, 'profile_title')}</h3>
                <p>{t(lang, 'profile_subtitle')}</p>
            </div>
        </div>
        <div class="profile-grid">
            {rows}
        </div>
    </div>
    """


def build_overview_html(incident_id: str | None, lang: str, text_size: str, contrast: bool) -> str:
    classes = get_accessibility_classes(text_size, contrast)
    if not incident_id or incident_id not in INCIDENT_MAP:
        return f"""
        <div class="panel-card workspace-card {classes}">
            <h3>{t(lang, 'summary_title')}</h3>
            <p class="empty-state">{t(lang, 'empty_overview')}</p>
        </div>
        """

    incident = INCIDENT_MAP[incident_id]
    metric_payload = METRICS.get(incident_id, {})
    stats = metric_payload.get("current_stats", {})
    stat_items = [
        (t(lang, "latency"), format_number(stats.get("latency_ms", 0), "ms")),
        (t(lang, "error_rate"), format_number(stats.get("error_rate_pct", 0), "%")),
        (t(lang, "cpu"), format_number(stats.get("cpu_pct", 0), "%")),
        (t(lang, "requests"), format_number(stats.get("request_volume_rpm", 0), "rpm")),
    ]
    stat_html = "".join(
        [
            f"""
            <div class="stat-card">
                <div class="stat-label">{label}</div>
                <div class="stat-value">{value}</div>
            </div>
            """
            for label, value in stat_items
        ]
    )
    severity_color = SEVERITY_COLORS.get(incident["severity"], "#64748b")
    return f"""
    <div class="panel-card workspace-card {classes}">
        <div class="workspace-top">
            <div>
                <div class="eyebrow">{t(lang, 'affected_service')}</div>
                <h3>{incident['service']}</h3>
            </div>
            <span class="severity-pill" style="background:{severity_color};">{incident['severity']}</span>
        </div>
        <div class="info-grid">
            <div class="info-card">
                <div class="info-label">{t(lang, 'current_state')}</div>
                <div class="info-body">{incident[f'health_summary_{lang}']}</div>
            </div>
            <div class="info-card">
                <div class="info-label">{t(lang, 'recent_change')}</div>
                <div class="info-body">{incident[f'recent_change_{lang}']}</div>
            </div>
        </div>
        <div class="summary-block">
            <div class="info-label">{t(lang, 'summary_title')}</div>
            <p>{incident[f'summary_{lang}']}</p>
        </div>
        <div class="stat-grid">
            {stat_html}
        </div>
    </div>
    """


def build_dependencies_html(incident_id: str | None, lang: str, text_size: str, contrast: bool) -> str:
    classes = get_accessibility_classes(text_size, contrast)
    if not incident_id or incident_id not in METRICS:
        return f"""
        <div class="panel-card workspace-card {classes}">
            <h3>{t(lang, 'dependencies')}</h3>
            <p class="empty-state">{t(lang, 'empty_dependencies')}</p>
        </div>
        """

    dependencies = METRICS[incident_id].get("dependency_health", [])
    dependency_html = "".join(
        [
            f"""
            <div class="dependency-node">
                <div class="dependency-name">{item['name']}</div>
                <div class="dependency-status status-{item['status'].lower()}">{item['status']}</div>
                <div class="dependency-impact">{item[f'impact_{lang}']}</div>
            </div>
            """
            for item in dependencies
        ]
    )
    return f"""
    <div class="panel-card workspace-card {classes}">
        <div class="section-inline-title">{t(lang, 'dependencies')}</div>
        <div class="dependency-grid">{dependency_html}</div>
    </div>
    """


def build_hypotheses_html(incident_id: str | None, lang: str, text_size: str, contrast: bool) -> str:
    classes = get_accessibility_classes(text_size, contrast)
    items = HYPOTHESES.get(incident_id, [])
    if not items:
        return f"""
        <div class="panel-card workspace-card {classes}">
            <h3>{t(lang, 'hypotheses')}</h3>
            <p class="empty-state">{t(lang, 'empty_hypotheses')}</p>
        </div>
        """

    cards = []
    for item in items:
        risk_color = item.get("risk_color", "#64748b")
        cards.append(
            f"""
            <div class="hypothesis-card">
                <div class="hypothesis-top">
                    <div class="hypothesis-title">{item[f'title_{lang}']}</div>
                    <span class="confidence-pill" style="color:{risk_color}; border-color:{risk_color};">
                        {t(lang, 'confidence')}: {item['confidence_score']}%
                    </span>
                </div>
                <p>{item[f'explanation_{lang}']}</p>
                <div class="next-check"><strong>{t(lang, 'next_check')}:</strong> {item[f'recommended_action_{lang}']}</div>
            </div>
            """
        )
    return f"""
    <div class="panel-card workspace-card {classes}">
        <div class="hypothesis-grid">{''.join(cards)}</div>
    </div>
    """


def build_actions_html(incident_id: str | None, lang: str, text_size: str, contrast: bool) -> str:
    classes = get_accessibility_classes(text_size, contrast)
    items = HYPOTHESES.get(incident_id, [])
    if not items:
        return f"""
        <div class="panel-card workspace-card {classes}">
            <p class="empty-state">{t(lang, 'empty_hypotheses')}</p>
        </div>
        """

    actions = "".join(
        [
            f"""
            <div class="action-item">
                <div class="action-rank">{index + 1}</div>
                <div class="action-copy">
                    <div class="action-title">{item[f'title_{lang}']}</div>
                    <div class="action-text">{item[f'recommended_action_{lang}']}</div>
                </div>
            </div>
            """
            for index, item in enumerate(items[:3])
        ]
    )
    return f"""
    <div class="panel-card workspace-card {classes}">
        <div class="action-list">{actions}</div>
    </div>
    """


def build_empty_figure(title: str, lang: str, contrast: bool) -> go.Figure:
    font_color = "#0f172a"
    paper_bg = "#ffffff"
    plot_bg = "#ffffff"
    if contrast:
        font_color = "#020617"
    fig = go.Figure()
    fig.update_layout(
        template="plotly_white",
        title=title,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color=font_color, size=13),
        margin=dict(l=24, r=18, t=54, b=24),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                text=t(lang, "status_no_incident"),
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=14, color="#64748b"),
            )
        ],
    )
    return fig


def build_signal_figure(incident_id: str | None, lang: str, contrast: bool) -> go.Figure:
    if not incident_id or incident_id not in METRICS:
        return build_empty_figure(t(lang, "signals"), lang, contrast)
    payload = METRICS[incident_id]
    timestamps = payload["timestamps"]
    series = payload["series"]
    fig = make_subplots(rows=1, cols=2, subplot_titles=(t(lang, "latency"), t(lang, "error_rate")))
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=series["latency_ms"],
            mode="lines+markers",
            name=t(lang, "latency"),
            line=dict(color="#2563eb", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(37,99,235,0.10)",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=series["error_rate_pct"],
            mode="lines+markers",
            name=t(lang, "error_rate"),
            line=dict(color="#ea580c", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(234,88,12,0.10)",
        ),
        row=1,
        col=2,
    )
    fig.update_layout(
        template="plotly_white",
        title=t(lang, "signals"),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#0f172a", size=13),
        margin=dict(l=24, r=18, t=56, b=24),
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="right", x=1.0),
        height=320,
    )
    fig.update_xaxes(showgrid=False, tickangle=-35, linecolor="#e2e8f0")
    fig.update_yaxes(showgrid=True, gridcolor="#eef2f7", zerolinecolor="#eef2f7")
    return fig


def build_load_figure(incident_id: str | None, lang: str, contrast: bool) -> go.Figure:
    if not incident_id or incident_id not in METRICS:
        return build_empty_figure(t(lang, "load"), lang, contrast)
    payload = METRICS[incident_id]
    timestamps = payload["timestamps"]
    series = payload["series"]
    fig = make_subplots(rows=1, cols=2, subplot_titles=(t(lang, "cpu"), t(lang, "requests")))
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=series["cpu_pct"],
            mode="lines+markers",
            name=t(lang, "cpu"),
            line=dict(color="#0f766e", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(15,118,110,0.10)",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=timestamps,
            y=series["request_volume_rpm"],
            name=t(lang, "requests"),
            marker=dict(color="#7c3aed", opacity=0.82),
        ),
        row=1,
        col=2,
    )
    fig.update_layout(
        template="plotly_white",
        title=t(lang, "load"),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#0f172a", size=13),
        margin=dict(l=24, r=18, t=56, b=24),
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="right", x=1.0),
        height=320,
    )
    fig.update_xaxes(showgrid=False, tickangle=-35, linecolor="#e2e8f0")
    fig.update_yaxes(showgrid=True, gridcolor="#eef2f7", zerolinecolor="#eef2f7")
    return fig


def get_suggested_prompts(lang: str) -> List[str]:
    return [
        t(lang, "why_checkout"),
        t(lang, "recent_changes"),
        t(lang, "root_cause"),
        t(lang, "check_first"),
        t(lang, "security_concern"),
    ]


def get_copilot_intro(lang: str) -> List[Dict[str, str]]:
    return [{"role": "assistant", "content": t(lang, "assistant_intro")}]


def build_copilot_response(incident_id: str, lang: str, question: str) -> str:
    incident = INCIDENT_MAP[incident_id]
    top_hypothesis = HYPOTHESES.get(incident_id, [{}])[0]
    responses = incident["copilot_responses"]
    normalized = question.lower()
    if any(keyword in normalized for keyword in ["change", "changed", "recent", "modification", "change rec", "changement"]):
        return responses[f"changes_{lang}"]
    if any(keyword in normalized for keyword in ["root", "cause", "likely", "probable", "racine"]):
        return responses[f"root_cause_{lang}"]
    if any(keyword in normalized for keyword in ["check", "first", "verify", "verifier", "premier"]):
        return responses[f"check_first_{lang}"]
    if any(keyword in normalized for keyword in ["security", "abuse", "credential", "securite", "attaque"]):
        return responses[f"security_{lang}"]
    if any(keyword in normalized for keyword in ["why", "failing", "down", "latency", "timeout", "pourquoi", "echec"]):
        return responses[f"summary_{lang}"]
    fallback_title = top_hypothesis.get(f"title_{lang}", t(lang, "unavailable"))
    fallback_action = top_hypothesis.get(f"recommended_action_{lang}", t(lang, "unavailable"))
    return (
        f"{responses[f'summary_{lang}']} "
        f"{t(lang, 'next_check')}: {fallback_action}. "
        f"{t(lang, 'confidence')}: {top_hypothesis.get('confidence_score', 0)}% on {fallback_title}."
    )


def sync_ui(lang: str, selected_incident: str | None, text_size: str, contrast: bool, chat_open: bool):
    enabled = selected_incident is not None
    status_message = t(lang, "status_loaded" if enabled else "status_no_incident")
    status_mode = "healthy" if enabled else "neutral"
    prompts = get_suggested_prompts(lang)
    chat_value = get_copilot_intro(lang)
    launcher = f"● {t(lang, 'copilot')}" if chat_open or enabled else f"○ {t(lang, 'launcher')}"
    return (
        build_header_html(lang, text_size, contrast),
        build_status_html(status_message, lang, text_size, contrast, status_mode),
        build_section_heading(t(lang, "queue_title"), t(lang, "queue_subtitle")),
        build_incident_cards(selected_incident, lang, text_size, contrast),
        gr.update(choices=get_incident_choices(lang), label=t(lang, "incident_selector"), value=selected_incident),
        gr.update(label=t(lang, "language")),
        gr.update(label=t(lang, "text_size")),
        gr.update(label=t(lang, "contrast")),
        build_profile_html(lang, text_size, contrast),
        build_section_heading(t(lang, "summary_title"), t(lang, "summary_subtitle")),
        build_overview_html(selected_incident, lang, text_size, contrast),
        build_section_heading(t(lang, "signals"), t(lang, "signals_subtitle")),
        build_signal_figure(selected_incident, lang, contrast),
        build_section_heading(t(lang, "load"), t(lang, "load_subtitle")),
        build_load_figure(selected_incident, lang, contrast),
        build_section_heading(t(lang, "dependencies"), t(lang, "dependencies_subtitle")),
        build_dependencies_html(selected_incident, lang, text_size, contrast),
        build_section_heading(t(lang, "hypotheses"), t(lang, "hypotheses_subtitle")),
        build_hypotheses_html(selected_incident, lang, text_size, contrast),
        build_section_heading(t(lang, "actions"), t(lang, "actions_subtitle")),
        build_actions_html(selected_incident, lang, text_size, contrast),
        build_section_heading(t(lang, "copilot"), t(lang, "copilot_subtitle")),
        gr.update(value=chat_value, label=t(lang, "copilot")),
        gr.update(placeholder=t(lang, "copilot_placeholder"), interactive=enabled),
        gr.update(value=t(lang, "ask_button"), interactive=enabled),
        gr.update(value=prompts[0], interactive=enabled),
        gr.update(value=prompts[1], interactive=enabled),
        gr.update(value=prompts[2], interactive=enabled),
        gr.update(value=prompts[3], interactive=enabled),
        gr.update(value=prompts[4], interactive=enabled),
        gr.update(value=launcher),
        gr.update(visible=chat_open),
        build_footer_html(lang),
        chat_value,
    )


def update_incident_view(selected_incident: str | None, lang: str, text_size: str, contrast: bool):
    cards = build_incident_cards(selected_incident, lang, text_size, contrast)
    intro_history = get_copilot_intro(lang)
    if not selected_incident:
        yield (
            cards,
            build_overview_html(None, lang, text_size, contrast),
            build_signal_figure(None, lang, contrast),
            build_load_figure(None, lang, contrast),
            build_dependencies_html(None, lang, text_size, contrast),
            build_hypotheses_html(None, lang, text_size, contrast),
            build_actions_html(None, lang, text_size, contrast),
            intro_history,
            intro_history,
            build_status_html(t(lang, "status_no_incident"), lang, text_size, contrast, "neutral"),
            gr.update(interactive=False, placeholder=t(lang, "copilot_placeholder")),
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(value=f"○ {t(lang, 'launcher')}"),
        )
        return
    yield (
        cards,
        build_overview_html(None, lang, text_size, contrast),
        build_empty_figure(t(lang, "signals"), lang, contrast),
        build_empty_figure(t(lang, "load"), lang, contrast),
        build_dependencies_html(None, lang, text_size, contrast),
        build_hypotheses_html(None, lang, text_size, contrast),
        build_actions_html(None, lang, text_size, contrast),
        intro_history,
        intro_history,
        build_status_html(t(lang, "status_loading"), lang, text_size, contrast, "loading"),
        gr.update(interactive=False, placeholder=t(lang, "copilot_placeholder")),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(value=f"● {t(lang, 'copilot')}"),
    )
    time.sleep(0.25)
    yield (
        cards,
        build_overview_html(selected_incident, lang, text_size, contrast),
        build_signal_figure(selected_incident, lang, contrast),
        build_load_figure(selected_incident, lang, contrast),
        build_dependencies_html(selected_incident, lang, text_size, contrast),
        build_hypotheses_html(selected_incident, lang, text_size, contrast),
        build_actions_html(selected_incident, lang, text_size, contrast),
        intro_history,
        intro_history,
        build_status_html(t(lang, "status_loaded"), lang, text_size, contrast, "healthy"),
        gr.update(interactive=True, placeholder=t(lang, "copilot_placeholder")),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(value=f"● {t(lang, 'copilot')}"),
    )


def toggle_chat(chat_open: bool, lang: str):
    next_state = not chat_open
    label = t(lang, "copilot") if next_state else t(lang, "launcher")
    prefix = "●" if next_state else "○"
    return next_state, gr.update(visible=next_state), gr.update(value=f"{prefix} {label}")


def submit_chat(
    message: str,
    history: List[Dict[str, str]] | None,
    selected_incident: str | None,
    lang: str,
    text_size: str,
    contrast: bool,
):
    history = history or []
    if not selected_incident:
        history.append({"role": "assistant", "content": t(lang, "status_chat_blocked")})
        return history, history, "", build_status_html(t(lang, "status_chat_blocked"), lang, text_size, contrast, "warning")
    if not message or not message.strip():
        return history, history, "", build_status_html(t(lang, "status_no_question"), lang, text_size, contrast, "warning")
    answer = build_copilot_response(selected_incident, lang, message.strip())
    history.append({"role": "user", "content": message.strip()})
    history.append({"role": "assistant", "content": answer})
    return history, history, "", build_status_html(t(lang, "status_loaded"), lang, text_size, contrast, "healthy")


def use_prompt(
    prompt: str,
    history: List[Dict[str, str]] | None,
    selected_incident: str | None,
    lang: str,
    text_size: str,
    contrast: bool,
):
    return submit_chat(prompt, history, selected_incident, lang, text_size, contrast)


CUSTOM_CSS = """
:root {
  --bg: #f5f7fb;
  --bg-soft: #eef2f7;
  --panel: #ffffff;
  --panel-soft: #fbfcfe;
  --panel-accent: #f2f7ff;
  --text: #0f172a;
  --text-soft: #475569;
  --text-faint: #64748b;
  --border: #e6ebf2;
  --border-strong: #d4dce8;
  --accent: #2563eb;
  --accent-soft: #dbeafe;
  --success: #15803d;
  --warning: #b45309;
  --danger: #dc2626;
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 12px 32px rgba(15, 23, 42, 0.06);
  --radius-xl: 18px;
  --radius-lg: 16px;
  --radius-md: 12px;
}

body, .gradio-container {
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.035), transparent 26%),
    linear-gradient(180deg, #f8fafc 0%, #f5f7fb 100%);
  color: var(--text);
}

.gradio-container {
  max-width: 1560px !important;
  padding: 20px 18px 28px !important;
}

.gradio-container .block,
.gradio-container .gr-box,
.gradio-container .gr-group {
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
}

.gradio-container button,
.gradio-container input,
.gradio-container textarea,
.gradio-container select,
.gradio-container label,
.gradio-container div,
.gradio-container span,
.gradio-container p {
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

.app-shell {
  gap: 16px !important;
}

.topbar-shell {
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border);
  border-radius: 18px;
  box-shadow: var(--shadow-sm);
  padding: 14px 18px;
  display: grid;
  grid-template-columns: 1.3fr 1fr 0.9fr;
  align-items: center;
  gap: 18px;
}

.brand-cluster,
.account-cluster {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-mark {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(180deg, #eff6ff, #dbeafe);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 14px;
}

.brand-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
}

.brand-subtitle {
  margin-top: 2px;
  font-size: 12px;
  color: var(--text-faint);
}

.nav-cluster {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.nav-item {
  padding: 8px 12px;
  border-radius: 10px;
  color: var(--text-faint);
  font-size: 13px;
  font-weight: 600;
  border: 1px solid transparent;
}

.nav-item.active {
  background: var(--panel-accent);
  color: var(--accent);
  border-color: #bfdbfe;
}

.account-meta {
  margin-left: auto;
  text-align: right;
}

.account-label {
  font-size: 11px;
  color: var(--text-faint);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 700;
}

.account-value {
  margin-top: 3px;
  font-size: 13px;
  color: var(--text-soft);
}

.account-avatar,
.profile-avatar {
  width: 38px;
  height: 38px;
  border-radius: 999px;
  background: #eff6ff;
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.settings-shell,
.status-shell,
.pane-shell,
.panel-card,
.chat-popup {
  background: var(--panel);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.settings-shell {
  border-radius: 16px;
  padding: 14px 16px 8px;
}

.status-shell {
  border-radius: 16px;
  padding: 16px 18px;
}

.status-label,
.eyebrow,
.info-label,
.stat-label,
.profile-key,
.dependency-impact {
  font-size: 11px;
  color: var(--text-faint);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 700;
}

.status-value {
  margin-top: 8px;
  font-size: 15px;
  color: var(--text);
  font-weight: 700;
}

.mode-healthy .status-value { color: var(--success); }
.mode-warning .status-value { color: var(--warning); }
.mode-loading .status-value { color: var(--accent); }

.section-heading {
  padding: 2px 2px 10px;
}

.section-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text);
}

.section-subtitle {
  margin-top: 3px;
  font-size: 12px;
  color: var(--text-faint);
}

.master-detail {
  gap: 16px !important;
  align-items: start !important;
}

.pane-shell {
  border-radius: 18px;
  padding: 14px;
}

.incident-card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 10px;
  transition: border-color 0.16s ease, background 0.16s ease, box-shadow 0.16s ease;
}

.incident-card:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-sm);
}

.incident-card.selected {
  background: var(--panel-accent);
  border-color: #93c5fd;
  box-shadow: inset 3px 0 0 var(--accent);
}

.incident-card-top,
.workspace-top,
.hypothesis-top,
.profile-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}

.incident-title,
.hypothesis-title,
.action-title {
  margin-top: 10px;
  color: var(--text);
  font-weight: 700;
  font-size: 15px;
  line-height: 1.35;
}

.incident-meta,
.incident-description,
.info-body,
.summary-block p,
.hypothesis-card p,
.next-check,
.action-text,
.profile-summary p,
.empty-state {
  color: var(--text-soft);
  font-size: 13px;
  line-height: 1.55;
}

.incident-meta,
.incident-description {
  margin-top: 7px;
  color: var(--text-faint);
  font-size: 12px;
}

.severity-pill,
.status-pill,
.confidence-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  padding: 4px 9px;
  font-size: 11px;
  font-weight: 700;
}

.severity-pill {
  color: white;
}

.status-pill,
.confidence-pill {
  background: #ffffff;
  border: 1px solid var(--border-strong);
}

.workspace-card,
.profile-card {
  border-radius: 16px;
  padding: 18px;
}

.workspace-card h3,
.profile-summary h3 {
  margin: 0;
  font-size: 16px;
  color: var(--text);
}

.info-grid,
.stat-grid,
.dependency-grid,
.hypothesis-grid,
.workspace-two-up {
  display: grid;
  gap: 14px;
}

.info-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin: 18px 0;
}

.stat-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
  margin-top: 18px;
}

.dependency-grid,
.hypothesis-grid {
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.info-card,
.stat-card,
.dependency-node,
.hypothesis-card,
.action-item,
.profile-row {
  background: var(--panel-soft);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px;
}

.stat-value {
  margin-top: 8px;
  font-size: 21px;
  font-weight: 700;
  color: var(--text);
}

.summary-block {
  margin-top: 2px;
}

.section-inline-title {
  margin-bottom: 14px;
  font-size: 14px;
  font-weight: 700;
  color: var(--text);
}

.dependency-name,
.profile-value {
  color: var(--text);
  font-weight: 600;
}

.dependency-status {
  margin: 8px 0;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.status-healthy { color: #15803d; }
.status-degraded { color: #c2410c; }
.status-failed { color: #dc2626; }
.status-monitoring { color: #2563eb; }

.profile-grid,
.action-list {
  display: grid;
  gap: 10px;
  margin-top: 16px;
}

.profile-top {
  align-items: center;
}

.profile-summary p {
  margin: 4px 0 0;
  font-size: 12px;
}

.profile-row,
.action-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.action-rank {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex: 0 0 auto;
}

.workspace-section {
  gap: 14px !important;
}

.plot-shell {
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
}

.settings-shell label,
.settings-shell .wrap label,
.settings-shell .label-wrap > label {
  color: var(--text-faint) !important;
  font-size: 12px !important;
  font-weight: 600 !important;
}

.settings-shell .gradio-dropdown > div,
.settings-shell .gradio-radio label,
.settings-shell .gradio-checkbox label,
.queue-select .gradio-radio label {
  background: #ffffff !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  box-shadow: none !important;
  color: var(--text) !important;
}

.queue-select .gradio-radio label.selected {
  border-color: #93c5fd !important;
  background: var(--accent-soft) !important;
}

.floating-launcher {
  position: fixed !important;
  right: 24px;
  bottom: 24px;
  z-index: 40;
}

.floating-launcher button {
  border-radius: 999px !important;
  padding: 12px 16px !important;
  background: #0f172a !important;
  color: white !important;
  border: none !important;
  box-shadow: var(--shadow-md) !important;
  font-weight: 700 !important;
}

.chat-panel-shell {
  position: fixed !important;
  right: 24px;
  bottom: 84px;
  z-index: 45;
  width: 360px;
  max-width: calc(100vw - 32px);
}

.chat-popup {
  border-radius: 18px;
  padding: 14px;
  box-shadow: var(--shadow-md);
}

.chat-shell {
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  background: var(--panel-soft);
}

.chat-shell .message.user {
  background: var(--accent-soft) !important;
  border: 1px solid #bfdbfe !important;
  border-radius: 14px !important;
}

.chat-shell .message.bot {
  background: #ffffff !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
}

.copilot-input textarea {
  background: #ffffff !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}

.send-btn button {
  background: #0f172a !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 700 !important;
}

.chat-close button {
  background: #ffffff !important;
  color: var(--text-soft) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}

.prompt-chip button {
  background: #ffffff !important;
  color: var(--text-soft) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  font-size: 12px !important;
}

.footer-shell {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 4px 0;
  color: var(--text-faint);
  font-size: 12px;
}

.footer-left {
  font-weight: 700;
  color: var(--text-soft);
}

.contrast-on.topbar-shell,
.contrast-on.status-shell,
.contrast-on.pane-shell,
.contrast-on.panel-card,
.contrast-on.chat-popup {
  border-color: #0f172a !important;
}

.size-compact { font-size: 0.95rem; }
.size-comfortable { font-size: 1rem; }
.size-large { font-size: 1.08rem; }

@media (max-width: 1280px) {
  .topbar-shell {
    grid-template-columns: 1fr;
  }

  .nav-cluster {
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .account-meta {
    margin-left: 0;
    text-align: left;
  }

  .stat-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .info-grid,
  .stat-grid,
  .dependency-grid,
  .hypothesis-grid {
    grid-template-columns: 1fr;
  }

  .chat-panel-shell {
    right: 12px;
    left: 12px;
    width: auto;
  }

  .floating-launcher {
    right: 12px;
    bottom: 12px;
  }
}
"""


with gr.Blocks(
    title="SentinelOps",
    css=CUSTOM_CSS,
    theme=gr.themes.Base(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        radius_size="md",
        text_size="md",
    ),
) as demo:
    chat_state = gr.State(get_copilot_intro("en"))
    chat_open_state = gr.State(False)

    with gr.Column(elem_classes=["app-shell"]):
        header_html = gr.HTML(build_header_html("en", "comfortable", False))

        with gr.Row(equal_height=False):
            with gr.Column(scale=7, min_width=620):
                status_html = gr.HTML(build_status_html(t("en", "status_no_incident"), "en", "comfortable", False, "neutral"))
            with gr.Column(scale=5, min_width=420):
                with gr.Group(elem_classes=["settings-shell"]):
                    with gr.Row():
                        language = gr.Dropdown(
                            choices=[("EN", "en"), ("FR", "fr")],
                            value="en",
                            label=t("en", "language"),
                            scale=1,
                        )
                        text_size = gr.Radio(
                            choices=["compact", "comfortable", "large"],
                            value="comfortable",
                            label=t("en", "text_size"),
                            scale=1,
                        )
                        contrast = gr.Checkbox(value=False, label=t("en", "contrast"), scale=1)

        with gr.Row(equal_height=False, elem_classes=["master-detail"]):
            with gr.Column(scale=3, min_width=310, elem_classes=["pane-shell"]):
                queue_heading = gr.HTML(build_section_heading(t("en", "queue_title"), t("en", "queue_subtitle")))
                incident_cards = gr.HTML(build_incident_cards(None, "en", "comfortable", False))
                incident_selector = gr.Radio(
                    choices=get_incident_choices("en"),
                    value=None,
                    label=t("en", "incident_selector"),
                    elem_classes=["queue-select"],
                )

            with gr.Column(scale=9, min_width=760):
                with gr.Row(equal_height=False):
                    with gr.Column(scale=8, min_width=520, elem_classes=["pane-shell"]):
                        summary_heading = gr.HTML(build_section_heading(t("en", "summary_title"), t("en", "summary_subtitle")))
                        overview_html = gr.HTML(build_overview_html(None, "en", "comfortable", False))

                        signals_heading = gr.HTML(build_section_heading(t("en", "signals"), t("en", "signals_subtitle")))
                        signal_chart = gr.Plot(build_signal_figure(None, "en", False), elem_classes=["plot-shell"])

                        load_heading = gr.HTML(build_section_heading(t("en", "load"), t("en", "load_subtitle")))
                        load_chart = gr.Plot(build_load_figure(None, "en", False), elem_classes=["plot-shell"])

                    with gr.Column(scale=4, min_width=320):
                        profile_html = gr.HTML(build_profile_html("en", "comfortable", False))
                        with gr.Group(elem_classes=["pane-shell"]):
                            deps_heading = gr.HTML(build_section_heading(t("en", "dependencies"), t("en", "dependencies_subtitle")))
                            dependencies_html = gr.HTML(build_dependencies_html(None, "en", "comfortable", False))

                with gr.Row(equal_height=False):
                    with gr.Column(scale=7, min_width=420, elem_classes=["pane-shell"]):
                        hypotheses_heading = gr.HTML(build_section_heading(t("en", "hypotheses"), t("en", "hypotheses_subtitle")))
                        hypotheses_html = gr.HTML(build_hypotheses_html(None, "en", "comfortable", False))
                    with gr.Column(scale=5, min_width=320, elem_classes=["pane-shell"]):
                        actions_heading = gr.HTML(build_section_heading(t("en", "actions"), t("en", "actions_subtitle")))
                        actions_html = gr.HTML(build_actions_html(None, "en", "comfortable", False))

        footer_html = gr.HTML(build_footer_html("en"))

        chat_launcher = gr.Button(t("en", "launcher"), elem_classes=["floating-launcher"])
        with gr.Column(visible=False, elem_classes=["chat-panel-shell"]) as chat_popup:
            with gr.Group(elem_classes=["chat-popup"]):
                copilot_heading = gr.HTML(build_section_heading(t("en", "copilot"), t("en", "copilot_subtitle")))
                chatbot = gr.Chatbot(
                    value=get_copilot_intro("en"),
                    type="messages",
                    height=360,
                    label=t("en", "copilot"),
                    elem_classes=["chat-shell"],
                )
                copilot_input = gr.Textbox(
                    show_label=False,
                    placeholder=t("en", "copilot_placeholder"),
                    interactive=False,
                    elem_classes=["copilot-input"],
                )
                with gr.Row():
                    send_button = gr.Button(t("en", "ask_button"), variant="primary", interactive=False, elem_classes=["send-btn"])
                    close_chat = gr.Button(t("en", "close_chat"), elem_classes=["chat-close"])
                with gr.Row():
                    prompt_one = gr.Button(t("en", "why_checkout"), interactive=False, elem_classes=["prompt-chip"])
                    prompt_two = gr.Button(t("en", "recent_changes"), interactive=False, elem_classes=["prompt-chip"])
                with gr.Row():
                    prompt_three = gr.Button(t("en", "root_cause"), interactive=False, elem_classes=["prompt-chip"])
                    prompt_four = gr.Button(t("en", "check_first"), interactive=False, elem_classes=["prompt-chip"])
                prompt_five = gr.Button(t("en", "security_concern"), interactive=False, elem_classes=["prompt-chip"])

    incident_selector.change(
        fn=update_incident_view,
        inputs=[incident_selector, language, text_size, contrast],
        outputs=[
            incident_cards,
            overview_html,
            signal_chart,
            load_chart,
            dependencies_html,
            hypotheses_html,
            actions_html,
            chat_state,
            chatbot,
            status_html,
            copilot_input,
            send_button,
            prompt_one,
            prompt_two,
            prompt_three,
            prompt_four,
            prompt_five,
            close_chat,
            chat_launcher,
        ],
    )

    for trigger in [language.change, text_size.change, contrast.change]:
        trigger(
            fn=sync_ui,
            inputs=[language, incident_selector, text_size, contrast, chat_open_state],
            outputs=[
                header_html,
                status_html,
                queue_heading,
                incident_cards,
                incident_selector,
                language,
                text_size,
                contrast,
                profile_html,
                summary_heading,
                overview_html,
                signals_heading,
                signal_chart,
                load_heading,
                load_chart,
                deps_heading,
                dependencies_html,
                hypotheses_heading,
                hypotheses_html,
                actions_heading,
                actions_html,
                copilot_heading,
                chatbot,
                copilot_input,
                send_button,
                prompt_one,
                prompt_two,
                prompt_three,
                prompt_four,
                prompt_five,
                chat_launcher,
                chat_popup,
                footer_html,
                chat_state,
            ],
        )

    chat_launcher.click(
        fn=toggle_chat,
        inputs=[chat_open_state, language],
        outputs=[chat_open_state, chat_popup, chat_launcher],
    )
    close_chat.click(
        fn=toggle_chat,
        inputs=[chat_open_state, language],
        outputs=[chat_open_state, chat_popup, chat_launcher],
    )

    send_button.click(
        fn=submit_chat,
        inputs=[copilot_input, chat_state, incident_selector, language, text_size, contrast],
        outputs=[chat_state, chatbot, copilot_input, status_html],
    )
    copilot_input.submit(
        fn=submit_chat,
        inputs=[copilot_input, chat_state, incident_selector, language, text_size, contrast],
        outputs=[chat_state, chatbot, copilot_input, status_html],
    )
    prompt_one.click(
        fn=use_prompt,
        inputs=[prompt_one, chat_state, incident_selector, language, text_size, contrast],
        outputs=[chat_state, chatbot, copilot_input, status_html],
    )
    prompt_two.click(
        fn=use_prompt,
        inputs=[prompt_two, chat_state, incident_selector, language, text_size, contrast],
        outputs=[chat_state, chatbot, copilot_input, status_html],
    )
    prompt_three.click(
        fn=use_prompt,
        inputs=[prompt_three, chat_state, incident_selector, language, text_size, contrast],
        outputs=[chat_state, chatbot, copilot_input, status_html],
    )
    prompt_four.click(
        fn=use_prompt,
        inputs=[prompt_four, chat_state, incident_selector, language, text_size, contrast],
        outputs=[chat_state, chatbot, copilot_input, status_html],
    )
    prompt_five.click(
        fn=use_prompt,
        inputs=[prompt_five, chat_state, incident_selector, language, text_size, contrast],
        outputs=[chat_state, chatbot, copilot_input, status_html],
    )


if __name__ == "__main__":
    demo.launch()
