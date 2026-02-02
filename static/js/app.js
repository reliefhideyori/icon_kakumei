/**
 * アイコン革命 - Client-side JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const motifInput = document.getElementById('motif');
    const generateBtn = document.getElementById('generate-btn');
    const resultPlaceholder = document.getElementById('result-placeholder');
    const resultContent = document.getElementById('result-content');
    const resultError = document.getElementById('result-error');
    const resultImage = document.getElementById('result-image');
    const resultMotif = document.getElementById('result-motif');
    const resultEnglish = document.getElementById('result-english');
    const resultStyle = document.getElementById('result-style');
    const downloadBtn = document.getElementById('download-btn');
    const errorMessage = document.getElementById('error-message');
    const faqItems = document.querySelectorAll('.faq-item');

    let currentImageData = null;
    let currentMotif = '';

    // ==========================================
    // FAQ Toggle
    // ==========================================
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            // Close other items
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            // Toggle current item
            item.classList.toggle('active');
        });
    });

    // ==========================================
    // Icon Generation
    // ==========================================

    // Generate button click
    generateBtn.addEventListener('click', async () => {
        const motif = motifInput.value.trim();
        const style = document.querySelector('input[name="style"]:checked').value;

        if (!motif) {
            showError('モチーフを入力してください');
            return;
        }

        await generateIcon(motif, style);
    });

    // Enter key to generate
    motifInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            generateBtn.click();
        }
    });

    // Download button
    downloadBtn.addEventListener('click', () => {
        if (!currentImageData) return;

        const link = document.createElement('a');
        link.href = currentImageData;
        link.download = `icon_${currentMotif.replace(/\s+/g, '_')}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    // Generate icon API call
    async function generateIcon(motif, style) {
        setLoading(true);
        hideAllResults();

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ motif, style }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || '生成に失敗しました');
            }

            // Show result
            currentImageData = data.image;
            currentMotif = data.motif;

            resultImage.src = data.image;
            resultMotif.textContent = data.motif;
            resultEnglish.textContent = data.english_motif;
            resultStyle.textContent = data.style;

            showResult();

        } catch (error) {
            showError(error.message);
        } finally {
            setLoading(false);
        }
    }

    // Set loading state
    function setLoading(isLoading) {
        generateBtn.disabled = isLoading;
        generateBtn.classList.toggle('loading', isLoading);
    }

    // Hide all results
    function hideAllResults() {
        resultPlaceholder.style.display = 'none';
        resultContent.style.display = 'none';
        resultError.style.display = 'none';
    }

    // Show result
    function showResult() {
        resultContent.style.display = 'flex';
    }

    // Show error
    function showError(message) {
        errorMessage.textContent = message;
        resultError.style.display = 'flex';
    }

    // ==========================================
    // Smooth scroll for anchor links
    // ==========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
