// ========================================================================
// CÓDIGO MILIONÁRIO — SCRIPT DO RANKING WEB (SUPABASE INTEGRATION)
// ========================================================================

// Credenciais públicas (Publishable / Anon Key)
// Nota de Segurança: A chave anon é segura para uso no frontend (browser),
// pois o acesso aos dados sensíveis é protegido via Row Level Security (RLS)
// e intermediado exclusivamente pela RPC 'buscar_ranking'.
const SUPABASE_URL = "https://joxqgnuoizhebanhygom.supabase.co";
const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_IbAxqtzO8_IWJvoH3EKOJw_WU2yeTvf";

// Inicialização do cliente Supabase
let client = null;
try {
    if (window.supabase && typeof window.supabase.createClient === "function") {
        client = window.supabase.createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY);
    } else {
        console.error("Biblioteca Supabase JS não foi carregada corretamente.");
    }
} catch (err) {
    console.error("Erro ao inicializar cliente Supabase:", err);
}

// Elementos da interface
const rankingList = document.getElementById("ranking-list");
const statusMessage = document.getElementById("status-message");
const lastUpdated = document.getElementById("last-updated");
const refreshButton = document.getElementById("refresh-button");

/**
 * Formata um valor numérico para o padrão de moeda brasileira (R$ X.XXX,XX)
 */
function formatarDinheiro(valor) {
    return Number(valor || 0).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

/**
 * Formata a quantidade de segundos no formato legível: "Xmin YYs"
 */
function formatarTempo(segundos) {
    const total = Math.floor(Number(segundos || 0));
    const minutos = Math.floor(total / 60);
    const resto = total % 60;

    if (minutos > 0) {
        return `${minutos}min ${String(resto).padStart(2, "0")}s`;
    }
    return `${resto}s`;
}

/**
 * Formata a data ISO para o padrão brasileiro DD/MM/AAAA
 */
function formatarData(dataISO) {
    if (!dataISO) return "-";
    try {
        const data = new Date(dataISO);
        return data.toLocaleDateString("pt-BR", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric"
        });
    } catch {
        return "-";
    }
}

/**
 * Sanitiza texto para prevenir injeções de HTML/XSS
 */
function escaparHTML(texto) {
    if (texto === null || texto === undefined) return "";
    return String(texto).replace(/[&<>"']/g, caractere => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[caractere]);
}

/**
 * Retorna o ícone ou medalha para as primeiras colocações
 */
function obterMedalha(posicao) {
    if (posicao === 1) return '<span class="badge-medal">🥇</span>';
    if (posicao === 2) return '<span class="badge-medal">🥈</span>';
    if (posicao === 3) return '<span class="badge-medal">🥉</span>';
    return '';
}

/**
 * Consulta a função RPC 'buscar_ranking' no Supabase e renderiza o Top 10
 */
async function carregarRanking() {
    if (!client) {
        rankingList.innerHTML = `
            <div class="message error">
                Não foi possível conectar ao Supabase. Verifique se o script da biblioteca carregou com sucesso.
            </div>
        `;
        if (statusMessage) {
            statusMessage.textContent = "Erro de inicialização do cliente Supabase.";
            statusMessage.className = "status-message error";
        }
        return;
    }

    rankingList.innerHTML = `
        <div class="message loading">
            <span class="spinner"></span>
            <span>Carregando classificação oficial...</span>
        </div>
    `;

    if (statusMessage) {
        statusMessage.textContent = "";
        statusMessage.className = "status-message";
    }

    if (refreshButton) {
        refreshButton.disabled = true;
    }

    try {
        // Chamada da RPC segura 'buscar_ranking'
        const { data, error } = await client.rpc("buscar_ranking");

        if (error) {
            throw error;
        }

        if (!data || data.length === 0) {
            rankingList.innerHTML = `
                <div class="message">
                    Nenhuma partida registrada ainda. Seja o primeiro a jogar!
                </div>
            `;
            if (statusMessage) {
                statusMessage.textContent = "Ranking vazio no momento.";
                statusMessage.className = "status-message";
            }
            return;
        }

        // Renderiza cada linha do ranking
        rankingList.innerHTML = data.map((jogador, index) => {
            const posicao = jogador.posicao || (index + 1);
            const medalha = obterMedalha(posicao);
            const topClass = posicao <= 3 ? `top-${posicao}` : "";
            const isPerfect = Number(jogador.acertos) === 9;
            const scoreClass = isPerfect ? "score score-perfect" : "score";

            return `
                <div class="ranking-row ${topClass}">
                    <span class="position">${medalha} ${posicao}º</span>
                    <span class="player" title="${escaparHTML(jogador.apelido)}">${escaparHTML(jogador.apelido)}</span>
                    <span class="prize">${formatarDinheiro(jogador.valor_ganho)}</span>
                    <span class="${scoreClass}">${jogador.acertos !== undefined ? jogador.acertos : '-'}/9</span>
                    <span class="time">${formatarTempo(jogador.tempo_segundos)}</span>
                    <span class="date">${formatarData(jogador.data_hora)}</span>
                </div>
            `;
        }).join("");

        const agora = new Date();
        const horaFormatada = agora.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit", second: "2-digit" });

        if (statusMessage) {
            statusMessage.textContent = `Ranking atualizado com sucesso (${data.length} jogadores listados).`;
            statusMessage.className = "status-message success";
        }

        if (lastUpdated) {
            lastUpdated.textContent = `Última sincronização: hoje às ${horaFormatada}`;
        }

    } catch (error) {
        console.error("Erro ao carregar o ranking:", error);
        rankingList.innerHTML = `
            <div class="message error">
                Não foi possível carregar o ranking no momento.
            </div>
        `;
        if (statusMessage) {
            statusMessage.textContent = "Falha ao consultar o banco de dados. Verifique sua conexão com a internet.";
            statusMessage.className = "status-message error";
        }
    } finally {
        if (refreshButton) {
            refreshButton.disabled = false;
        }
    }
}

// Event Listeners
if (refreshButton) {
    refreshButton.addEventListener("click", carregarRanking);
}

// Carregamento inicial ao abrir a página
carregarRanking();
