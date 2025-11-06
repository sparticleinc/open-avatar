// 引入核心库
const script0 = document.createElement('script');
script0.src = 'https://cubism.live2d.com/sdk-web/cubismcore/live2dcubismcore.min.js';
const script2 = document.createElement('script');
script2.src = 'https://cdn.jsdelivr.net/npm/pixi.js@7.x/dist/pixi.min.js';
const script5 = document.createElement('script');
script5.src = 'https://cdn.jsdelivr.net/gh/RaSan147/pixi-live2d-display@v0.5.0-ls-7/dist/cubism4.min.js';

let loadedScripts = 0;
const totalScripts = 3;
let model4, app;

const cubism4Model = "runtime/haru_greeter_t05.model3.json";

function notifyLoadComplete() {
    // 触发自定义事件
    const loadCompleteEvent = new CustomEvent('animeModuleLoaded', {
        detail: {
            message: 'Anime avatar module loaded successfully',
            timestamp: new Date().toISOString()
        }
    });
    document.dispatchEvent(loadCompleteEvent);
    // 回调
    if (window.onAnimeModuleLoaded && typeof window.onAnimeModuleLoaded === 'function') {
        window.onAnimeModuleLoaded({
            message: 'Anime avatar module loaded successfully',
            timestamp: new Date().toISOString()
        });
    }
}

async function initializeAvatar() {
    app = new PIXI.Application({
        view: document.getElementById("canvas"),
        autoStart: true,
        resizeTo: window,
        backgroundAlpha: 0,
    });    
    model4 = await PIXI.live2d.Live2DModel.from(cubism4Model);
    app.stage.addChild(model4);
    model4.scale.set(0.2);
    model4.anchor.set(0.5, 0.5);
    model4.x = app.renderer.width / 2;
    model4.y = app.renderer.height / 2;
    
    // 窗口大小改变时重新居中
    window.addEventListener('resize', () => {
        model4.x = app.renderer.width / 2;
        model4.y = app.renderer.height / 2;
    });
}

async function checkAllScriptsLoaded() {
    loadedScripts++;
    console.log(`Script ${loadedScripts}/${totalScripts} loaded`);
    if (loadedScripts === totalScripts) {
        console.log('All scripts loaded successfully! Initializing avatar...');
        await initializeAvatar();
        notifyLoadComplete();
    }
}

// 顺序加载依赖脚本
script0.onload = () => {
    checkAllScriptsLoaded();
    document.head.appendChild(script2);
};
script2.onload = () => {
    checkAllScriptsLoaded();
    document.head.appendChild(script5);
};
script5.onload = () => {
    checkAllScriptsLoaded();
};
document.head.appendChild(script0);

