<script lang="ts">
    import "./SubPage_Write.scss";

    import { post } from "query";
    import { pop } from "svelte-spa-router";

    let title = "";
    let content = "";
    let category = "";

    let selectedFiles = [];

    const handleSubmit = async () => {
        await post(title, content, category, selectedFiles)
          .then(res => {
            if (res) {
              pop();
            }
            else {
              console.log("err");
            }
          })
          .catch(err => {
            console.log(err);
          });
    }

    function handleUpload(event) {
      selectedFiles = Array.from(event.target.files);
    }
</script>

<div class="container_write">
    <h1>글 쓰기</h1>
    <form class="form" on:submit|preventDefault={handleSubmit}>
      <label>
        제목:
        <input type="text" class="input_title" bind:value={title} />
      </label>
      <label>
        카테고리:
        <input class="input_category" bind:value={category} />
      </label>
      <textarea class="content" bind:value={content}></textarea>
      <div class="input_element">
        <label>
          사진 및 파일:
          <input type="file" multiple on:change={handleUpload} />
        </label>
      </div>
      <button class="submit">글 쓰기</button>
    </form>
</div>