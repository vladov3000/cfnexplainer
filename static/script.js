"use strict";

async function onUpload() {
    const fileInput = document.getElementById("fileInput");
    const files     = fileInput.files;

    if (fileInput.files.length === 0) {
	return;
    }

    const uploadText   = document.querySelector("#uploadButton span");
    const loadingImage = document.querySelector("#uploadButton img");

    uploadText.style.display   = "none";
    loadingImage.style.display = "block";
    
    await fetch("/upload", {
	method: "POST",
	body: fileInput.files[0],
    });

    uploadText.style.display   = "block";
    loadingImage.style.display = "none";    
}

async function onQuery() {
    const queryInput = document.getElementById("queryInput");
    const query      = queryInput.value;

    const queryText    = document.querySelector("#queryButton span");
    const loadingImage = document.querySelector("#queryButton img");

    queryText.style.display    = "none";
    loadingImage.style.display = "block";
    
    const response = await fetch(`/query?query=${query}`);
    const result   = await response.text();

    queryText.style.display    = "block";
    loadingImage.style.display = "none";

    const content    = document.getElementsByClassName("queryContainer")[0];
    const resultSpan = document.createElement("span");
    resultSpan.classList.add("bubble");
    resultSpan.textContent = result;
    content.after(resultSpan);
}

function initialize() {
    const uploadButton = document.getElementById("uploadButton");
    uploadButton.addEventListener("click", onUpload);

    const queryButton = document.getElementById("queryButton");
    queryButton.addEventListener("click", onQuery);
}

window.onload = initialize;
