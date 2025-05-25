/**
 * Xử lý lỗi ảnh
 */

document.addEventListener('DOMContentLoaded', function() {
    // Xử lý tất cả các ảnh trong trang
    var images = document.querySelectorAll('img');
    
    images.forEach(function(img) {
        img.addEventListener('error', function() {
            console.log('Lỗi tải ảnh:', this.src);
            
            // Kiểm tra xem ảnh đã là ảnh mặc định chưa để tránh vòng lặp vô hạn
            if (!this.src.includes('default_image.jpg')) {
                this.src = '/static/images/default_image.jpg';
            } else {
                // Nếu ngay cả ảnh mặc định cũng lỗi, hiển thị placeholder
                this.style.display = 'none';
                
                // Tạo một placeholder
                var placeholder = document.createElement('div');
                placeholder.className = 'image-placeholder';
                placeholder.textContent = 'Không có ảnh';
                placeholder.style.width = '100%';
                placeholder.style.height = '200px';
                placeholder.style.backgroundColor = '#f0f0f0';
                placeholder.style.display = 'flex';
                placeholder.style.alignItems = 'center';
                placeholder.style.justifyContent = 'center';
                placeholder.style.color = '#666';
                placeholder.style.border = '1px solid #ddd';
                
                // Chèn placeholder vào ngay trước img
                this.parentNode.insertBefore(placeholder, this);
            }
        });
    });
}); 