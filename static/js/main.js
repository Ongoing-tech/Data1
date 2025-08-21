// 全局变量
let currentPage = 1;
let currentFilters = {};
let chart = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadSuppliers();
    loadData();
    
    // 绑定表单提交事件
    document.getElementById('filterForm').addEventListener('submit', function(e) {
        e.preventDefault();
        currentPage = 1;
        currentFilters = getFormData();
        loadData();
        // 如果图表正在显示，也更新图表数据
        const chartContainer = document.getElementById('chartContainer');
        if (chartContainer.style.display !== 'none') {
            loadChartData();
        }
    });
    
    // 绑定重置按钮事件
    document.querySelector('button[type="reset"]')?.addEventListener('click', function() {
        document.getElementById('filterForm').reset();
        currentPage = 1;
        currentFilters = {};
        loadData();
        // 如果图表正在显示，也更新图表数据
        const chartContainer = document.getElementById('chartContainer');
        if (chartContainer.style.display !== 'none') {
            loadChartData();
        }
    });
});

// 获取表单数据
function getFormData() {
    const formData = new FormData(document.getElementById('filterForm'));
    const filters = {};
    
    for (let [key, value] of formData.entries()) {
        if (value.trim()) {
            filters[key] = value.trim();
        }
    }
    
    return filters;
}

// 加载供应商列表
async function loadSuppliers() {
    try {
        const response = await fetch('/api/suppliers');
        const result = await response.json();
        
        if (result.code === 200) {
            const select = document.getElementById('supplier');
            select.innerHTML = '<option value="">全部供应商</option>';
            
            result.data.forEach(supplier => {
                const option = document.createElement('option');
                option.value = supplier;
                option.textContent = supplier;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('加载供应商列表失败:', error);
    }
}

// 加载数据
async function loadData() {
    showLoading(true);
    
    try {
        const params = new URLSearchParams({
            page: currentPage,
            per_page: 20,
            ...currentFilters
        });
        
        const response = await fetch(`/api/data?${params}`);
        const result = await response.json();
        
        if (result.code === 200) {
            renderTable(result.data.items);
            renderPagination(result.data);
            updatePaginationInfo(result.data);
        } else {
            showAlert('加载数据失败: ' + result.message, 'danger');
        }
    } catch (error) {
        console.error('加载数据失败:', error);
        showAlert('加载数据失败，请检查网络连接', 'danger');
    } finally {
        showLoading(false);
    }
}

// 渲染表格
function renderTable(data) {
    const tbody = document.getElementById('dataTableBody');
    tbody.innerHTML = '';
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" class="text-center text-muted">暂无数据</td></tr>';
        return;
    }
    
    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.date}</td>
            <td><strong>${item.sku}</strong></td>
            <td>${item.product_name || '-'}</td>
            <td>${item.inbound_quantity || 0}</td>
            <td>${item.outbound_quantity || 0}</td>
            <td><span class="badge bg-primary">${item.inventory_balance || 0}</span></td>
            <td>${item.supplier || '-'}</td>
            <td>${item.operator || '-'}</td>
            <td>${item.remarks || '-'}</td>
        `;
        tbody.appendChild(row);
    });
}

// 渲染分页
function renderPagination(data) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';
    
    if (data.pages <= 1) return;
    
    // 上一页
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${data.page === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${data.page - 1})">上一页</a>`;
    pagination.appendChild(prevLi);
    
    // 页码
    const startPage = Math.max(1, data.page - 2);
    const endPage = Math.min(data.pages, data.page + 2);
    
    if (startPage > 1) {
        const firstLi = document.createElement('li');
        firstLi.className = 'page-item';
        firstLi.innerHTML = `<a class="page-link" href="#" onclick="goToPage(1)">1</a>`;
        pagination.appendChild(firstLi);
        
        if (startPage > 2) {
            const ellipsisLi = document.createElement('li');
            ellipsisLi.className = 'page-item disabled';
            ellipsisLi.innerHTML = '<span class="page-link">...</span>';
            pagination.appendChild(ellipsisLi);
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === data.page ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${i})">${i}</a>`;
        pagination.appendChild(li);
    }
    
    if (endPage < data.pages) {
        if (endPage < data.pages - 1) {
            const ellipsisLi = document.createElement('li');
            ellipsisLi.className = 'page-item disabled';
            ellipsisLi.innerHTML = '<span class="page-link">...</span>';
            pagination.appendChild(ellipsisLi);
        }
        
        const lastLi = document.createElement('li');
        lastLi.className = 'page-item';
        lastLi.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${data.pages})">${data.pages}</a>`;
        pagination.appendChild(lastLi);
    }
    
    // 下一页
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${data.page === data.pages ? 'disabled' : ''}`;
    nextLi.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${data.page + 1})">下一页</a>`;
    pagination.appendChild(nextLi);
}

// 更新分页信息
function updatePaginationInfo(data) {
    const start = (data.page - 1) * data.per_page + 1;
    const end = Math.min(data.page * data.per_page, data.total);
    
    document.getElementById('paginationInfo').textContent = 
        `显示第 ${start}-${end} 项，共 ${data.total} 项`;
}

// 跳转到指定页
function goToPage(page) {
    currentPage = page;
    loadData();
}

// 显示/隐藏加载状态
function showLoading(show) {
    const loading = document.getElementById('loading');
    const tableContainer = document.getElementById('tableContainer');
    
    if (show) {
        loading.style.display = 'block';
        tableContainer.style.display = 'none';
    } else {
        loading.style.display = 'none';
        tableContainer.style.display = 'block';
    }
}

// 显示提示信息
function showAlert(message, type = 'info') {
    // 创建提示框
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // 3秒后自动关闭
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 3000);
}

// 显示图表
async function showChart() {
    const chartContainer = document.getElementById('chartContainer');
    
    if (chartContainer.style.display === 'none') {
        chartContainer.style.display = 'block';
        await loadChartData();
    } else {
        chartContainer.style.display = 'none';
    }
}

// 加载图表数据
async function loadChartData() {
    try {
        const params = new URLSearchParams(currentFilters);
        const response = await fetch(`/api/chart-data?${params}`);
        const result = await response.json();
        
        if (result.code === 200) {
            renderChart(result.data);
        } else {
            showAlert('加载图表数据失败: ' + result.message, 'danger');
        }
    } catch (error) {
        console.error('加载图表数据失败:', error);
        showAlert('加载图表数据失败，请检查网络连接', 'danger');
    }
}

// 渲染图表
function renderChart(data) {
    const chartDom = document.getElementById('chart');
    
    if (chart) {
        chart.dispose();
    }
    
    chart = echarts.init(chartDom);
    
    const option = {
        title: {
            text: '库存余额变化趋势',
            left: 'center',
            textStyle: {
                fontSize: 16,
                fontWeight: 'bold'
            }
        },
        tooltip: {
            trigger: 'axis',
            formatter: function(params) {
                const date = params[0].axisValue;
                const value = params[0].value;
                return `${date}<br/>库存余额: ${value.toLocaleString()}`;
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: data.dates,
            axisLabel: {
                rotate: 45
            }
        },
        yAxis: {
            type: 'value',
            name: '库存余额',
            axisLabel: {
                formatter: function(value) {
                    return value.toLocaleString();
                }
            }
        },
        series: [{
            name: '库存余额',
            type: 'line',
            data: data.balances,
            smooth: true,
            lineStyle: {
                color: '#007bff',
                width: 2
            },
            itemStyle: {
                color: '#007bff'
            },
            areaStyle: {
                color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [{
                        offset: 0,
                        color: 'rgba(0, 123, 255, 0.3)'
                    }, {
                        offset: 1,
                        color: 'rgba(0, 123, 255, 0.1)'
                    }]
                }
            }
        }]
    };
    
    chart.setOption(option);
    
    // 响应式调整
    window.addEventListener('resize', function() {
        chart.resize();
    });
}