// frontend/static/js/app.js

// 获取 DOM 元素
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const fileInput = document.getElementById('fileInput');
const uploadStatus = document.querySelector('.upload-status');

// 发送问题的函数
function sendQuestion() {
    const question = userInput.value.trim();
    if (question === '') {
        alert('请输入问题！');
        return;
    }

    // 显示用户消息
    addMessage('user-message', question);

    // 清空输入框
    userInput.value = '';

    // 发送问题到后端
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        if (data.answer) {
            addMessage('bot-message', data.answer);
        } else {
            addMessage('bot-message', '抱歉，我没有找到相关的答案。');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('bot-message', '抱歉，出现了错误，请稍后再试。');
    });
}

// 添加消息到聊天框
function addMessage(type, text) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);
    messageDiv.textContent = text;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight; // 滚动到最底部
}

// 处理文件上传
fileInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (!file) {
        return;
    }

    // 显示上传状态
    uploadStatus.textContent = '正在上传...';

    // 创建 FormData 对象
    const formData = new FormData();
    formData.append('file', file);

    // 发送文件到后端
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            uploadStatus.textContent = '上传成功！';
            addMessage('bot-message', '文件上传成功，您可以开始提问了。');
        } else {
            uploadStatus.textContent = '上传失败，请重试。';
            addMessage('bot-message', '文件上传失败，请稍后再试。');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        uploadStatus.textContent = '上传失败，请重试。';
        addMessage('bot-message', '文件上传失败，请稍后再试。');
    });
});