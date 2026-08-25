import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_dfd_diagram(output_path="c:/Users/migue/Faculdade/PB_IA_TP1/others/dfd_api.png"):
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Background color
    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")

    # Title
    ax.text(50, 97, "DATA FLOW DIAGRAM (DFD) & MODELAGEM DE SEGURANÇA - API FASTAPI",
            fontsize=15, fontweight="bold", ha="center", color="#0f172a")
    ax.text(50, 94.5, "Trabalho Prático 1 (TP1) - Projeto de Bloco | Análise de Trust Boundaries e Tríade CIA",
            fontsize=10, ha="center", color="#475569", style="italic")

    # -------------------------------------------------------------
    # TRUST BOUNDARY 1: ZONA PÚBLICA / NÃO AUTENTICADA (EXTERNA)
    # -------------------------------------------------------------
    tb1 = patches.FancyBboxPatch((2, 48), 26, 43, boxstyle="round,pad=1",
                                 facecolor="#fee2e2", edgecolor="#ef4444", linestyle="--", linewidth=2, alpha=0.6)
    ax.add_patch(tb1)
    ax.text(15, 89, "TRUST BOUNDARY 1\n(Zona Não Confiável / Pública)",
            fontsize=10, fontweight="bold", ha="center", color="#991b1b")

    # Entidades Externas
    client_box = patches.FancyBboxPatch((4, 73), 22, 10, boxstyle="square,pad=0.3",
                                        facecolor="#ffffff", edgecolor="#1e293b", linewidth=1.5)
    ax.add_patch(client_box)
    ax.text(15, 79, "[E1] Cliente / Suporte", fontsize=10, fontweight="bold", ha="center", color="#0f172a")
    ax.text(15, 75.5, "Envia tickets de texto\npara classificação", fontsize=8, ha="center", color="#334155")

    admin_box = patches.FancyBboxPatch((4, 53), 22, 10, boxstyle="square,pad=0.3",
                                       facecolor="#ffffff", edgecolor="#1e293b", linewidth=1.5)
    ax.add_patch(admin_box)
    ax.text(15, 59, "[E2] Administrador", fontsize=10, fontweight="bold", ha="center", color="#0f172a")
    ax.text(15, 55.5, "Credenciais (login/senha)\npara autenticação", fontsize=8, ha="center", color="#334155")

    # -------------------------------------------------------------
    # TRUST BOUNDARY 2: PERÍMETRO DA API FASTAPI (INGRESS / GATEWAY)
    # -------------------------------------------------------------
    tb2 = patches.FancyBboxPatch((32, 48), 32, 43, boxstyle="round,pad=1",
                                 facecolor="#fef3c7", edgecolor="#f59e0b", linestyle="-.", linewidth=2, alpha=0.5)
    ax.add_patch(tb2)
    ax.text(48, 89, "FASTAPI INGRESS / AUTH LAYER\n(Borda de Autenticação)",
            fontsize=10, fontweight="bold", ha="center", color="#b45309")

    # Processo P1: Health Check (Público)
    p1 = patches.Circle((48, 77), 5.5, facecolor="#e0f2fe", edgecolor="#0284c7", linewidth=1.8)
    ax.add_patch(p1)
    ax.text(48, 77.8, "P1", fontsize=10, fontweight="bold", ha="center", color="#0369a1")
    ax.text(48, 75.5, "GET /health", fontsize=8, fontweight="bold", ha="center", color="#0369a1")

    # Processo P2: Autenticação JWT
    p2 = patches.Circle((48, 57), 5.5, facecolor="#ede9fe", edgecolor="#7c3aed", linewidth=1.8)
    ax.add_patch(p2)
    ax.text(48, 57.8, "P2", fontsize=10, fontweight="bold", ha="center", color="#6d28d9")
    ax.text(48, 55.5, "POST /auth/token", fontsize=8, fontweight="bold", ha="center", color="#6d28d9")

    # -------------------------------------------------------------
    # TRUST BOUNDARY 3: ZONA INTERNA SEGURA (PROTEGIDA POR JWT)
    # -------------------------------------------------------------
    tb3 = patches.FancyBboxPatch((68, 48), 30, 43, boxstyle="round,pad=1",
                                 facecolor="#dcfce7", edgecolor="#16a34a", linestyle="-", linewidth=2, alpha=0.5)
    ax.add_patch(tb3)
    ax.text(83, 89, "TRUST BOUNDARY 2\n(Zona Protegida por JWT)",
            fontsize=10, fontweight="bold", ha="center", color="#15803d")

    # Processo P3: Validador JWT (Middleware / Depends)
    p3 = patches.Circle((76, 73), 4.5, facecolor="#fef08a", edgecolor="#ca8a04", linewidth=1.8)
    ax.add_patch(p3)
    ax.text(76, 73.8, "P3", fontsize=9, fontweight="bold", ha="center", color="#854d0e")
    ax.text(76, 71.8, "OAuth2/JWT\nValidation", fontsize=7, ha="center", color="#854d0e")

    # Processo P4: Predição
    p4 = patches.Circle((90, 73), 4.5, facecolor="#bbf7d0", edgecolor="#16a34a", linewidth=1.8)
    ax.add_patch(p4)
    ax.text(90, 73.8, "P4", fontsize=9, fontweight="bold", ha="center", color="#166534")
    ax.text(90, 71.8, "POST /predict\n(Mock Model)", fontsize=7, ha="center", color="#166534")

    # Data Store D1: Credenciais In-Code
    ds1_top = patches.Rectangle((70, 53), 26, 0.2, facecolor="#334155")
    ds1_bot = patches.Rectangle((70, 59), 26, 0.2, facecolor="#334155")
    ax.add_patch(ds1_top)
    ax.add_patch(ds1_bot)
    ax.text(83, 56.5, "[D1] Credenciais Admin (In-Code)", fontsize=8, fontweight="bold", ha="center", color="#1e293b")
    ax.text(83, 54.5, "Hash Bcrypt + Secret Key HS256", fontsize=7.5, ha="center", color="#475569")

    # Fluxos de Dados (Setas e Anotações)
    # Admin -> P2 (Credenciais)
    ax.annotate("1. Form (user/pwd)", xy=(42.5, 57), xytext=(26, 57),
                arrowprops=dict(facecolor="#475569", edgecolor="#475569", arrowstyle="->", lw=1.5),
                fontsize=7.5, color="#1e293b", va="bottom")

    # P2 <-> D1 (Verificação de Hash)
    ax.annotate("2. Valida Hash", xy=(70, 56.5), xytext=(53.5, 57),
                arrowprops=dict(facecolor="#7c3aed", edgecolor="#7c3aed", arrowstyle="<->", lw=1.3),
                fontsize=7.5, color="#6d28d9", va="bottom")

    # P2 -> Admin (Retorno do Token JWT)
    ax.annotate("3. Token JWT", xy=(26, 53), xytext=(43, 53),
                arrowprops=dict(facecolor="#16a34a", edgecolor="#16a34a", arrowstyle="->", lw=1.5),
                fontsize=7.5, color="#15803d", va="bottom")

    # Cliente -> P1 (Health Check)
    ax.annotate("Req Status", xy=(42.5, 77), xytext=(26, 77),
                arrowprops=dict(facecolor="#0284c7", edgecolor="#0284c7", arrowstyle="->", lw=1.2),
                fontsize=7.5, color="#0369a1", va="bottom")

    # Cliente -> P3 (Bearer Token + Payload)
    ax.annotate("4. Bearer JWT + Ticket Text", xy=(71.5, 75), xytext=(26, 81),
                arrowprops=dict(facecolor="#d97706", edgecolor="#d97706", arrowstyle="->", lw=1.5),
                fontsize=7.5, color="#b45309", va="bottom")

    # P3 -> P4 (Token Validado)
    ax.annotate("5. Autenticado", xy=(85.5, 73), xytext=(80.5, 73),
                arrowprops=dict(facecolor="#16a34a", edgecolor="#16a34a", arrowstyle="->", lw=1.5),
                fontsize=7, color="#166534", va="bottom")

    # P4 -> Cliente (Resposta com Intenção)
    ax.annotate("6. Resposta JSON {intent, confidence}", xy=(26, 70), xytext=(87, 67),
                arrowprops=dict(facecolor="#0f172a", edgecolor="#0f172a", arrowstyle="->", lw=1.3,
                                connectionstyle="arc3,rad=0.15"),
                fontsize=7.5, color="#0f172a", va="top")

    # -------------------------------------------------------------
    # TABELA / MATRIZ DA TRÍADE CIA
    # -------------------------------------------------------------
    table_card = patches.FancyBboxPatch((2, 3), 96, 41, boxstyle="round,pad=0.8",
                                        facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.5)
    ax.add_patch(table_card)
    ax.text(50, 41.5, "APLICAÇÃO DA TRÍADE CIA AOS COMPONENTES DO SISTEMA",
            fontsize=11, fontweight="bold", ha="center", color="#0f172a")

    # Cabeçalho da Tabela
    headers = ["Componente / Rota", "Confidencialidade (C)", "Integridade (I)", "Disponibilidade (A)"]
    x_positions = [4, 25, 52, 77]
    col_widths = [20, 26, 24, 20]

    header_bg = patches.Rectangle((3, 37.5), 94, 2.8, facecolor="#e2e8f0")
    ax.add_patch(header_bg)
    for pos, h in zip(x_positions, headers):
        ax.text(pos + 1, 38.8, h, fontsize=8.5, fontweight="bold", color="#1e293b", va="center")

    # Linhas da tabela
    rows = [
        (
            "[E1 / E2] Clientes & Admin\n(Entidades Externas)",
            "Alta: Credenciais de acesso e dados de\ntickets (PII) protegidos em trânsito (HTTPS).",
            "Média/Alta: Requisições não devem ser\nadulteradas (TLS + Headers íntegros).",
            "Média: Usuários devem conseguir alcançar a API sem bloqueios indevidos."
        ),
        (
            "GET /health\n(Processo P1)",
            "Baixa: Rota pública sem dados sigilosos,\nretorna apenas status e versão do serviço.",
            "Alta: A resposta deve refletir o estado real\nda aplicação sem manipulação.",
            "Crítica: Essencial para health checks,\nbalanceadores de carga e orquestradores."
        ),
        (
            "POST /auth/token\n(Processo P2 & JWT)",
            "Crítica: Senha protegida por Bcrypt; token\nassinado com SECRET_KEY inatingível.",
            "Crítica: Assinatura JWT impede forjação\nde identidade e elevação de privilégios.",
            "Alta: Sem autenticação funcional, nenhuma\nrota protegida pode ser consumida."
        ),
        (
            "POST /predict\n(Processo P3, P4 & ML)",
            "Alta: Textos de suporte podem conter PII;\napenas usuários autorizados têm acesso.",
            "Alta: Garantir que a classificação e score\nretornados correspondam à predição real.",
            "Alta: Atendimento depende da baixa latência\ne alta disponibilidade da inferência."
        ),
        (
            "[D1] Base In-Code / Chaves\n(Armazenamento de Dados)",
            "Crítica: Segredo JWT e credenciais nunca\ndevem vazar em logs, repositórios ou erros.",
            "Crítica: Constantes in-code não devem ser\nsobrescritas ou corrompidas em runtime.",
            "Alta: Dicionário em memória com acesso\ninstantâneo O(1) sem dependência externa."
        )
    ]

    y = 35.5
    for i, row in enumerate(rows):
        bg_col = "#f8fafc" if i % 2 == 0 else "#ffffff"
        row_bg = patches.Rectangle((3, y - 5.5), 94, 6.2, facecolor=bg_col)
        ax.add_patch(row_bg)
        
        ax.text(x_positions[0] + 0.5, y - 2.5, row[0], fontsize=7.5, fontweight="bold", color="#0f172a", va="center")
        ax.text(x_positions[1] + 0.5, y - 2.5, row[1], fontsize=7, color="#334155", va="center")
        ax.text(x_positions[2] + 0.5, y - 2.5, row[2], fontsize=7, color="#334155", va="center")
        ax.text(x_positions[3] + 0.5, y - 2.5, row[3], fontsize=7, color="#334155", va="center")
        y -= 6.4

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"DFD Diagram saved to {output_path}")

if __name__ == "__main__":
    create_dfd_diagram()
