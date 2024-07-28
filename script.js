document.addEventListener("DOMContentLoaded", function() {
    const imageInput = document.getElementById('imageInput');
    const captionType = document.getElementById('captionType');
    const manualCaption = document.getElementById('manualCaption');
    const aiPrompt = document.getElementById('aiPrompt');
    const positionSelect = document.getElementById('position');
    const fontSizeInput = document.getElementById('fontSize');
    const textColorInput = document.getElementById('textColor');
    const generateBtn = document.getElementById('generateBtn');
    const memeImage = document.getElementById('memeImage');

    // Enable/Disable input fields based on caption type
    captionType.addEventListener('change', function() {
        if (captionType.value === 'manual') {
            manualCaption.disabled = false;
            aiPrompt.disabled = true;
        } else {
            manualCaption.disabled = true;
            aiPrompt.disabled = false;
        }
    });

    // Generate meme on button click
    generateBtn.addEventListener('click', function() {
        const file = imageInput.files[0];
        if (!file) {
            alert("Please upload an image.");
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            const img = new Image();
            img.onload = function() {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);

                // Determine caption and position
                const caption = captionType.value === 'manual' ? manualCaption.value : generateAiCaption(aiPrompt.value);
                const position = positionSelect.value;
                const fontSize = fontSizeInput.value;
                const textColor = textColorInput.value;

                // Set font style
                ctx.font = '${fontSize}px Arial';
                ctx.fillStyle = textColor;

                // Adjust text position based on alignment
                const textWidth = ctx.measureText(caption).width;
                let x = canvas.width / 2;
                let y = canvas.height - 30;
                if (position === 'top') {
                    y = 30;
                } else if (position === 'left') {
                    x = 30;
                    y = canvas.height / 2;
                    ctx.textAlign = 'left';
                } else if (position === 'right') {
                    x = canvas.width - 30;
                    y = canvas.height / 2;
                    ctx.textAlign = 'right';
                } else {
                    ctx.textAlign = 'center';
                }

                // Wrap text if it exceeds the width of the image
                wrapText(ctx, caption, x, y, canvas.width, fontSize);

                memeImage.src = canvas.toDataURL();
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    });

    // Function to wrap text within the canvas width
    function wrapText(ctx, text, x, y, maxWidth, fontSize) {
        const words = text.split(' ');
        let line = '';
        const lineHeight = parseInt(fontSize, 10) * 1.2;

        for (let i = 0; i < words.length; i++) {
            const testLine = line + words[i] + ' ';
            const testWidth = ctx.measureText(testLine).width;
            if (testWidth > maxWidth - 20 && i > 0) {
                ctx.fillText(line, x, y);
                line = words[i] + ' ';
                y += lineHeight;
            } else {
                line = testLine;
            }
        }
        ctx.fillText(line, x, y);
    }

    // Placeholder function for AI caption generation
    function generateAiCaption(prompt) {
        // Replace this with actual AI model call
        return 'Generated caption for: ${prompt}';
    }
});