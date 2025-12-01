console.log("YouTube Extension Loaded");

// -------------------------
// Create floating button
// -------------------------
const floatingButton = document.createElement("button");
floatingButton.innerText = "🎶 Baixar Musica JOCA DJ";
floatingButton.style.position = "fixed";
floatingButton.style.bottom = "30px";
floatingButton.style.right = "30px";
floatingButton.style.zIndex = "999999";
floatingButton.style.padding = "10px 20px";
floatingButton.style.borderRadius = "8px";
floatingButton.style.background = "#ff0000";
floatingButton.style.color = "white";
floatingButton.style.fontSize = "25px";
floatingButton.style.border = "none";
floatingButton.style.cursor = "pointer";
floatingButton.style.boxShadow = "0px 0px 10px rgba(0,0,0,0.3)";

document.body.appendChild(floatingButton);

// -------------------------
// Send URL to Python endpoint
// -------------------------
function sendToPython() {
    const url = window.location.href;

    // ignore if not a real YouTube video page
    if (!url.includes("youtube.com/watch")) {
        alert("Só funciona em vídeos do YouTube Joca kkkk");
        return;
    }

    console.log("Sending:", url);

    fetch("http://192.168.0.112:5005/add?url=" + encodeURIComponent(url))
        .then(r => r.text())
        .then(t => {
            console.log("JOCA DJ respondeu:", t);
            floatingButton.innerText = "✅ Enviado para baixar!";
            setTimeout(() => {
                floatingButton.innerText = "🎶 Baixar Música JOCA DJ";
            }, 3000);
        })
        .catch(err => {
            console.error("Erro:", err);
            alert("Ai não Joca... Abre o programa JOCA DJ antes kkkk\n\n E não esquece do pendrive conectado kkkkk");
        });
}

floatingButton.addEventListener("click", sendToPython);
