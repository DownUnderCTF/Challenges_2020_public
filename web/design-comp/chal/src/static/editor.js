(function() {
    function initEditor() {
        const editor = ace.edit('editor');
        editor.session.setMode('ace/mode/css');
        editor.setTheme('ace/theme/tomorrow_night');
        editor.setFontSize('16px');
        editor.setKeyboardHandler('');
        editor.setValue(
            window.opener.document.getElementById('user-styles').textContent
        );

        return editor;
    }

    function ipc(msg) {
        if(!window.opener) { console.warn('No opener'); return; }
        window.opener.postMessage(msg);
    }

    const editor = initEditor();

    const bindingsElement = document.getElementById('key-bindings');
    bindingsElement.addEventListener('change', evt => {
        const bindings = bindingsElement.value;
        if(bindings == 'vim') {
            editor.setKeyboardHandler('ace/keyboard/vim');
        } else {
            editor.setKeyboardHandler('');
        }
    });

    document.getElementById('preview').addEventListener('click', () => {
        ipc({
            action: 'preview',
            css: editor.getValue()
        });
    });
})();