// 全局变量
let selectedFile = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const resetBtn = document.getElementById('resetBtn');
    
    // 点击上传区域触发文件选择
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    // 文件选择事件
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleFileSelect(file);
        }
    });
    
    // 拖拽事件
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    
    // 上传按钮事件
    uploadBtn.addEventListener('click', function() {
        if (selectedFile) {
            uploadFile();
        }
    });
    
    // 重置按钮事件
    resetBtn.addEventListener('click', function() {
        resetUpload();
    });
});

// 处理文件选择
function handleFileSelect(file) {
    // 验证文件类型
    if (!file.name.toLowerCase().endsWith('.xlsx')) {
        showAlert('请选择.xlsx格式的Excel文件', 'danger');
        return;
    }
    
    // 验证文件大小（2MB）
    if (file.size > 2 * 1024 * 1024) {
        showAlert('文件大小不能超过2MB', 'danger');
        return;
    }
    
    selectedFile = file;
    
    // 更新UI
    const uploadArea = document.getElementById('uploadArea');
    const fileInfo = document.getElementById('fileInfo');
    const fileDetails = document.getElementById('fileDetails');
    const uploadBtn = document.getElementById('uploadBtn');
    
    uploadArea.classList.add('has-file');
    uploadArea.innerHTML = `
        <i class="bi bi-file-earmark-excel" style="font-size: 3rem; color: #28a745;"></i>
        <h5 class="mt-3">${file.name}</h5>
        <p class="text-muted">文件大小: ${formatFileSize(file.size)}</p>
    `;
    
    fileDetails.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <strong>文件名:</strong> ${file.name}
            </div>
            <div class="col-md-6">
                <strong>文件大小:</strong> ${formatFileSize(file.size)}
            </div>
        </div>
        <div class="row mt-2">
            <div class="col-md-6">
                <strong>文件类型:</strong> ${file.type || 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
            </div>
            <div class="col-md-6">
                <strong>最后修改:</strong> ${new Date(file.lastModified).toLocaleString()}
            </div>
        </div>
    `;
    
    fileInfo.style.display = 'block';
    uploadBtn.disabled = false;
    resetBtn.style.display = 'inline-block';
    
    hideAlert();
}

// 上传文件
async function uploadFile() {
    if (!selectedFile) return;
    
    const uploadBtn = document.getElementById('uploadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const progressBar = document.getElementById('progressBar');
    const progress = document.getElementById('progress');
    
    // 禁用按钮
    uploadBtn.disabled = true;
    resetBtn.disabled = true;
    
    // 显示进度条
    progressBar.style.display = 'block';
    progress.style.width = '0%';
    progress.textContent = '0%';
    
    // 创建FormData
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        // 模拟进度
        let progressValue = 0;
        const progressInterval = setInterval(() => {
            progressValue += Math.random() * 30;
            if (progressValue >= 90) {
                progressValue = 90;
                clearInterval(progressInterval);
            }
            updateProgress(progressValue);
        }, 200);
        
        // 发送请求
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        clearInterval(progressInterval);
        updateProgress(100);
        
        const result = await response.json();
        
        if (result.code === 200) {
            showAlert(result.message, 'success');
            setTimeout(() => {
                resetUpload();
            }, 2000);
        } else {
            showAlert(result.message, 'danger');
            // 如果有详细错误信息，显示出来
            if (result.errors) {
                const errorDetails = result.errors.join('<br>');
                showAlert(`详细错误信息:<br>${errorDetails}`, 'warning');
            }
        }
        
    } catch (error) {
        console.error('上传失败:', error);
        showAlert('上传失败，请检查网络连接', 'danger');
    } finally {
        // 恢复按钮状态
        uploadBtn.disabled = false;
        resetBtn.disabled = false;
        
        // 3秒后隐藏进度条
        setTimeout(() => {
            progressBar.style.display = 'none';
        }, 3000);
    }
}

// 重置上传
function resetUpload() {
    selectedFile = null;
    
    const uploadArea = document.getElementById('uploadArea');
    const fileInfo = document.getElementById('fileInfo');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const progressBar = document.getElementById('progressBar');
    
    // 重置上传区域
    uploadArea.classList.remove('has-file');
    uploadArea.innerHTML = `
        <i class="bi bi-cloud-upload" style="font-size: 3rem; color: #6c757d;"></i>
        <h5 class="mt-3">拖拽文件到此处或点击选择文件</h5>
        <p class="text-muted">支持.xlsx格式文件，最大2MB</p>
        <input type="file" id="fileInput" accept=".xlsx" style="display: none;">
    `;
    
    // 重新绑定文件选择事件
    const newFileInput = uploadArea.querySelector('#fileInput');
    newFileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleFileSelect(file);
        }
    });
    
    // 隐藏文件信息
    fileInfo.style.display = 'none';
    
    // 重置按钮状态
    uploadBtn.disabled = true;
    resetBtn.style.display = 'none';
    
    // 隐藏进度条和提示
    progressBar.style.display = 'none';
    hideAlert();
}

// 更新进度条
function updateProgress(percent) {
    const progress = document.getElementById('progress');
    progress.style.width = percent + '%';
    progress.textContent = Math.round(percent) + '%';
}

// 显示提示信息
function showAlert(message, type = 'info') {
    const alertDiv = document.getElementById('alertMessage');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = message;
    alertDiv.style.display = 'block';
    
    // 滚动到提示信息位置
    alertDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// 隐藏提示信息
function hideAlert() {
    const alertDiv = document.getElementById('alertMessage');
    alertDiv.style.display = 'none';
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 防止页面刷新时的数据丢失
window.addEventListener('beforeunload', function(e) {
    if (selectedFile) {
        e.preventDefault();
        e.returnValue = '';
    }
});