document.addEventListener('DOMContentLoaded', () => {
    // --- Existing scroll and anchor code ---
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.feature-card, .step-card, .demo-card');
        const windowHeight = window.innerHeight;

        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const elementVisible = 150;
            if (elementPosition < windowHeight - elementVisible) {
                element.classList.add('visible');
            }
        });
    };

    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    feather.replace();

    // --- Upload button functionality ---
    const uploadButton = document.querySelector(
        'button.bg-primary.hover\\:bg-blue-600.text-white.px-8.py-3.rounded-full.text-lg.font-medium.transition-all.transform.hover\\:scale-105'
    );

    const previewImage = document.getElementById("preview-image");
    const detectedBrand = document.getElementById("detected-brand");
    const detectedConfidence = document.getElementById("detected-confidence");
    const demoCard = document.getElementById("demo-card");

    uploadButton.addEventListener('click', () => {
        // Create hidden file input
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.click();

        input.onchange = async () => {
            const file = input.files[0];
            if (!file) return;

            if (!file.type.startsWith("image/")) {
                alert("Please upload a valid image file.");
                return;
            }

            // Show preview
            previewImage.src = URL.createObjectURL(file);

            // Small animation on upload
            demoCard.classList.add("scale-95");
            setTimeout(() => demoCard.classList.remove("scale-95"), 150);

            // Prepare form data
            const formData = new FormData();
            formData.append("file", file);

            try {
                const response = await fetch("http://localhost:8000/predict", {
                    method: "POST",
                    body: formData
                });

                const result = await response.json();

                if (result.error) {
                    detectedBrand.textContent = "Error";
                    detectedConfidence.textContent = "—";
                    return;
                }

                // Update UI
                detectedBrand.textContent = result.predicted_class;
                detectedConfidence.textContent = result.confidence + "%";

                // Glow animation on update
                const glow = "shadow-[0_0_20px_rgba(59,130,246,0.7)]";
                demoCard.classList.add(glow);
                setTimeout(() => demoCard.classList.remove(glow), 800);

            } catch (err) {
                console.error(err);
                detectedBrand.textContent = "Server Error";
                detectedConfidence.textContent = "—";
            }
        };
    });
});
