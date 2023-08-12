<div class="container_loading">
    <div class="box_loading" />
    <div class="loader" />
</div>

<style>
    .container_loading {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;

        position: absolute;

        flex-direction: column;

        overflow: hidden;
    }
    .box_loading {
        width: 100%;
        height: 100%;

        position: absolute;

        background-color: black;
        opacity: 0.7;
    }
    .loader {
        margin: auto;
        border: 20px solid #EAF0F6;
        border-radius: 50%;
        border-top: 20px solid mediumaquamarine;
        width: 200px;
        height: 200px;
        animation: spinner 4s linear infinite;
    }

    @keyframes spinner {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
    }
</style>