(function () {
    'use strict'

    /* dropzone */
    let myDropzone = new Dropzone(".dropzone");
        myDropzone.on("addedfile", file => {
    });

    /* filepond */
    FilePond.registerPlugin(
        FilePondPluginImagePreview,
        FilePondPluginImageExifOrientation,
        FilePondPluginFileValidateSize,
        FilePondPluginFileEncode,
        FilePondPluginImageEdit,
        FilePondPluginFileValidateType,
        FilePondPluginImageCrop,
        FilePondPluginImageResize,
        FilePondPluginImageTransform
    );

    /* multiple upload */
    const MultipleElement = document.querySelector('.multiple-filepond');
    if (MultipleElement) FilePond.create(MultipleElement,);
    
    /* single upload */
    FilePond.create(
        document.querySelector('.single-fileupload'),
        {
            labelIdle: `عکس خود را بکشید و رها کنید یا <span class="filepond--label-action">مرور فایل ها</span>`,
            imagePreviewHeight: 170,
            imageCropAspectRatio: '1:1',
            imageResizeTargetWidth: 200,
            imageResizeTargetHeight: 200,
            stylePanelLayout: 'compact circle',
            styleLoadIndicatorPosition: 'center bottom',
            styleButtonRemoveItemPosition: 'center bottom'
        }
    );

})();