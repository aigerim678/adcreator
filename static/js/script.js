document.addEventListener('DOMContentLoaded', function() {
    // Select all dropdowns
    const dropdowns = document.querySelectorAll('.custom-dropdown');

    dropdowns.forEach(dropdown => {
        const button = dropdown.querySelector('.dropdown-button');
        const list = dropdown.querySelector('.dropdown-list');
        const items = dropdown.querySelectorAll('.dropdown-item');
        
        // Найдите соответствующий textarea внутри того же блока, что и dropdown
        const textarea = dropdown.closest('.scenario__item').querySelector('textarea');

        // Toggle dropdown visibility
        button.addEventListener('click', function(event) {
            event.stopPropagation();
            list.style.display = list.style.display === 'block' ? 'none' : 'block';
        });

        // При выборе пункта записываем текст в textarea и закрываем dropdown
        items.forEach(function(item) {
            item.addEventListener('click', function() {
                const selectedText = item.textContent;
                
                // Записываем текст в кнопку и textarea
                button.textContent = selectedText;
                if (textarea) {
                    textarea.value = selectedText; // Записываем текст выбранного пункта в textarea
                }

                // Закрываем dropdown
                list.style.display = 'none';
            });
        });
    });

    // Close all dropdowns if clicked outside
    document.addEventListener('click', function(event) {
        dropdowns.forEach(dropdown => {
            const list = dropdown.querySelector('.dropdown-list');
            if (!dropdown.contains(event.target)) {
                list.style.display = 'none';
            }
        });
    });
});




document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.querySelector('.button[type="submit"]');
    const errorMessage = document.getElementById('error-message');

    submitButton.addEventListener('click', function(event) {
        const textareas = document.querySelectorAll('.scenario__area textarea');
        let allFilled = true;

        textareas.forEach((textarea) => {
            if (textarea.value.trim() === '') {
                allFilled = false;
            }
        });

        if (!allFilled) {
            event.preventDefault(); // Предотвращаем отправку формы
            errorMessage.classList.remove('d-none'); // Показываем сообщение об ошибке

            setTimeout(() => {
                errorMessage.classList.add('d-none'); // Автоматически скрываем сообщение через 3 секунды
            }, 3000);
        }
    });
});








function openModal() {
    document.getElementById('modalContainer').style.display = 'flex';
}

function closeModal() {
    document.getElementById('modalContainer').style.display = 'none';
}


document.addEventListener('DOMContentLoaded', function () {
    const checkbox = document.getElementById('watched');
    const button = document.querySelector('.submit-button');

    checkbox.addEventListener('change', function() {
        if (checkbox.checked) {
            button.classList.remove('button-disabled');
            button.classList.add('button-filled');
            button.disabled = false;
        } else {
            button.classList.remove('button-filled');
            button.classList.add('button-disabled');
            button.disabled = true;
        }
    });
});



function uploadAudio() {
    const fileInput = document.getElementById('audioUpload');
    const file = fileInput.files[0];
    const csrfToken = document.getElementById('csrf_token').value;  // Получаем CSRF-токен
    
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch(uploadAudioUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken  // Добавляем CSRF-токен
            },
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert("Файл успешно загружен!");
                

                // Обновить состояние, чтобы показать сообщение о добавлении аудио
                sessionStorage.setItem('audioUploaded', 'true');
                
                // Перезагрузить страницу, чтобы обновить отображение элемента
                window.location.href = uploadVideoUrl;
            
            } else {
                alert("Ошибка загрузки файла.");
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });
    }
}






let mediaRecorder;
let audioChunks = [];
let audioBlob = null;  // Переменная для хранения аудиофайла после записи временно

function showRecordingControls() {
    document.getElementById('startRecordButton').style.display = 'none';
    document.getElementById('uploadButton').style.display = 'none';
    document.getElementById('recordingControls').style.display = 'flex';
}

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                console.log("Recording stopped and saved locally. Ready to upload.");
            };

            const recordButton = document.getElementById('recordButton');
            recordButton.style.backgroundColor = 'red'; // Меняем цвет фона на красный
            const recordingStatus = document.getElementById('recordingStatus');
            recordingStatus.style.display = 'block';
            recordingStatus.textContent = "Запись идет...";

            
            console.log("Recording started");
        })
        .catch(error => console.error("Error accessing microphone:", error));
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();

        const recordButton = document.getElementById('recordButton');
        recordButton.style.backgroundColor = ''; // Сбрасываем цвет фона
        const recordingStatus = document.getElementById('recordingStatus');
        recordingStatus.style.display = 'none';


        console.log("Recording stopped but not uploaded.");

    }
}

function pauseRecording() {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.pause();
        document.getElementById('pauseButton').style.display = 'none';
        document.getElementById('resumeButton').style.display = 'inline-block';
        const recordingStatus = document.getElementById('recordingStatus');
        recordingStatus.style.display = 'block';
        recordingStatus.textContent = "Пауза";
        console.log("Recording paused");

    }
}


function resumeRecording() {
    if (mediaRecorder && mediaRecorder.state === "paused") {
        mediaRecorder.resume();
        document.getElementById('resumeButton').style.display = 'none';
        document.getElementById('pauseButton').style.display = 'inline-block';

        
        recordingStatus.textContent = "Запись идет...";

        console.log("Recording resumed");
    }
}

function saveRecording() {
    if (audioBlob) {
        uploadRecordedAudio(audioBlob);  // Загружаем только если запись существует
    } else {
        alert("Нет записи для сохранения!");
    }
}

function resetUI() {
    
    document.getElementById('resumeButton').style.display = 'none';
}


function returnBack(){
    document.getElementById('startRecordButton').style.display = 'flex';
    document.getElementById('uploadButton').style.display = 'flex';
    document.getElementById('recordingControls').style.display = 'none';
}

function uploadRecordedAudio(audioBlob) {
    
    const csrfToken = document.getElementById('csrf_token').value;
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav');

    fetch(uploadAudioUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            alert("Запись успешно загружена!");
            // Сбросить переменную audioBlob после загрузки
            audioBlob = null;

            // Сохраняем состояние в sessionStorage
            sessionStorage.setItem('audioUploaded', 'true');

            // Перезагрузить страницу, чтобы обновить отображение элемента
            
            window.location.href = uploadVideoUrl;

        } else {
            alert("Ошибка загрузки записи.");
        }
    })
    .catch(error => {
        console.error("Ошибка при загрузке записи:", error);
    });
}






document.addEventListener('DOMContentLoaded', function () {
    const videoInput = document.getElementById('videoInput');
    const uploadSuccessMessage = document.getElementById('uploadSuccessMessage');

    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    videoInput.addEventListener('change', function () {
        if (videoInput.files.length > 0) {
            const selectedFile = videoInput.files[0];

            // Проверка размера файла (максимум 250 МБ)
            if (selectedFile.size <= 250 * 1024 * 1024) {
                // Создание объекта FormData и добавление выбранного файла
                const formData = new FormData();
                formData.append('video', selectedFile);


                // Отправка файла на сервер с помощью fetch
                fetch(uploadVideoUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    body: formData
                })
                .then(response => {
                    if (response.ok) {
                        // Показать сообщение об успешной загрузке
                        uploadSuccessMessage.style.display = 'block';
                    } else {
                        alert("Ошибка загрузки файла. Пожалуйста, попробуйте снова.");
                    }
                })
                .catch(error => {
                    console.error("Ошибка:", error);
                    alert("Ошибка при отправке файла. Пожалуйста, попробуйте снова.");
                });
            } else {
                alert('Файл слишком большой. Пожалуйста, выберите файл размером не более 250 МБ.');
            }
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const retryButton = document.getElementById("retry-button");
    const form = document.getElementById("ask-ai-form");
    const userMessage = document.getElementById("user-message");

    // Обработчик нажатия на кнопку "Попробовать еще раз"
    if (retryButton) {
        retryButton.addEventListener("click", function () {
            // Получаем сохраненное сообщение из localStorage
            const message = localStorage.getItem("userMessage");
            const source = localStorage.getItem("formSource");

            if (message && source) {
                // Создаем форму динамически
                const form = document.createElement("form");
                form.method = "POST";
                form.action = generateResponseUrl;

                // Создаем поле для CSRF токена
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                const csrfInput = document.createElement("input");
                csrfInput.type = "hidden";
                csrfInput.name = "csrfmiddlewaretoken";
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);

                // Создаем поле для сообщения пользователя
                const messageInput = document.createElement("textarea");
                messageInput.name = "user_message";
                messageInput.style.display = "none"; // Скрываем поле
                messageInput.value = message;
                form.appendChild(messageInput);

                // Создаем поле для source, чтобы определить, откуда пришел запрос
                const sourceInput = document.createElement("input");
                sourceInput.type = "hidden";
                sourceInput.name = "source";
                sourceInput.value = source;
                form.appendChild(sourceInput);

                // Добавляем форму в DOM и отправляем
                document.body.appendChild(form);
                form.submit();
            } else {
                alert("Пожалуйста, введите сообщение для AI.");
            }
        });
    }

    // Сохраняем сообщение и источник формы в localStorage для повторного использования
    if (form) {
        form.addEventListener("submit", function () {
            if (userMessage && userMessage.value.trim()) {
                localStorage.setItem("userMessage", userMessage.value.trim());
            }
            // Сохраняем источник из скрытого поля формы
            const sourceInput = form.querySelector('input[name="source"]');
            if (sourceInput) {
                localStorage.setItem("formSource", sourceInput.value);
            }
        });
    }

    
});





document.addEventListener("DOMContentLoaded", function () {
    // Находим все элементы с классом bot__item
    const botItems = document.querySelectorAll('.bot__item');

    botItems.forEach(item => {
        item.addEventListener('click', function () {
            // Получаем текст элемента
            const textToCopy = item.innerText;

            // Копируем текст в буфер обмена
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Создаем уведомление (alert)
                const alertBox = document.createElement('div');
                alertBox.innerText = 'Текст скопирован';
                alertBox.style.position = 'fixed';
                alertBox.style.bottom = '20px';
                alertBox.style.left = '50%';
                alertBox.style.transform = 'translateX(-50%)';
                alertBox.style.backgroundColor = '#4CAF50';
                alertBox.style.color = '#fff';
                alertBox.style.padding = '10px 20px';
                alertBox.style.borderRadius = '5px';
                alertBox.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.2)';
                alertBox.style.zIndex = '1000';

                // Добавляем уведомление на страницу
                document.body.appendChild(alertBox);

                // Удаляем уведомление через 1 секунду
                setTimeout(() => {
                    alertBox.remove();
                }, 1000);
            }).catch(err => {
                console.error('Ошибка при копировании текста: ', err);
            });
        });
    });
});






