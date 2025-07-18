document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileInput");
    const fileLabel = document.querySelector('label[for="fileInput"]');

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            fileLabel.textContent = file.name;

            // Display video duration and resolution for MP4 files
            if (file.type === "video/mp4") {
                const video = document.createElement("video");
                video.preload = "metadata";
                video.src = URL.createObjectURL(file);
                video.onloadedmetadata = function () {
                    const duration = Math.round(video.duration);
                    const resolution = video.videoWidth + "x" + video.videoHeight;
                    document.getElementById("fileInfo").innerHTML = `Duration: ${duration}s, Resolution: ${resolution}`;
                    URL.revokeObjectURL(video.src);
                };
            } else {
                document.getElementById("fileInfo").textContent = "";
            }
        } else {
            fileLabel.textContent = "Choose File";
            document.getElementById("fileInfo").textContent = "";
        }
    });

    document.getElementById("uploadForm").addEventListener("submit", function (e) {
        e.preventDefault();

        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        const compressBtn = document.getElementById("compressBtn");
        const btnText = compressBtn.querySelector(".btn-text");
        const btnLoading = compressBtn.querySelector(".btn-loading");
        btnText.style.display = "none";
        btnLoading.style.display = "inline-block";

        const progressContainer = document.getElementById("progressContainer");
        const progressBar = document.getElementById("progressBar");
        const progressText = document.getElementById("progressText");
        const resultArea = document.getElementById("resultArea");

        progressContainer.style.display = "block";
        progressBar.style.width = "0%";
        progressText.textContent = "0%";

        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/compress", true);

        xhr.upload.onprogress = function (e) {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                progressBar.style.width = percent + "%";
                progressText.textContent = percent + "%";
            }
        };

        xhr.onload = function () {
            btnText.style.display = "inline-block";
            btnLoading.style.display = "none";

            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);

                // Show results
                document.getElementById("originalSize").textContent = data.original_size + " MB";
                document.getElementById("compressedSize").textContent = data.compressed_size + " MB";
                document.getElementById("reductionPercent").textContent = data.reduction + "%";
                document.getElementById("downloadBtn").href = `/download/${data.filename}`;

                resultArea.style.display = "block";
                document.getElementById("uploadArea").style.display = "none";
            } else {
                alert("Something went wrong! Try again.");
            }
        };

        xhr.send(formData);
    });

    document.getElementById("newFileBtn").addEventListener("click", () => {
        location.reload();
    });
});
