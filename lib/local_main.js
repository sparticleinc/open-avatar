// 动态加载脚本的函数
function loadScript(url) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = url;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

// 按顺序加载所需的脚本
async function loadDependencies() {
    const scripts = ['runtime/anime_runtime.js'];

    for (const script of scripts) {
        await loadScript(script);
    }
    
    // 等待anime模块完全加载完成
    await new Promise((resolve) => {
        const handleLoadComplete = (event) => {
            console.log('Live2D model loaded:', event.detail);
            document.removeEventListener('animeModuleLoaded', handleLoadComplete);
            resolve();
        };
        
        // 监听anime模块加载完成事件
        document.addEventListener('animeModuleLoaded', handleLoadComplete);
        
        // 设置超时，防止无限等待
        setTimeout(() => {
            console.warn('Live2D model load timeout, proceeding anyway');
            document.removeEventListener('animeModuleLoaded', handleLoadComplete);
            resolve();
        }, 30000); // 30秒超时
    });
}

// 开始加载依赖项
loadDependencies().catch(error => {
    console.error('Failed to load dependencies:', error);
});
