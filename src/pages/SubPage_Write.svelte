<script lang="ts">
    import "./SubPage_Write.scss";

    import { post, get_content, type IPost, modify_content } from "query";
    import { pop } from "svelte-spa-router";

    let title = "";
    let content = "";
    let selected_category;

    let categories = [
      { id: 1, text: "프로젝트", category: "active" },
      { id: 2, text: "구인구직", category: "hellowork"},
      { id: 3, text:  "예산", category: "budget" }
    ];

    let selectedFiles = [];

    export let params: { content_id: string } = { content_id: "" };

    const handleSubmit = async () => {
      if(params.content_id === "") {
        await post(title, content, selected_category.category, selectedFiles)
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
      else {
        await modify_content(params.content_id, title, content, selected_category.category)
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
    }

    function handleUpload(event) {
      selectedFiles = Array.from(event.target.files);
    }

    let data: IPost = null;
    const get_data = async (content_id: string) => {
        get_content(content_id)
            .then(res => {
                if(data !== null || data !== undefined) {
                  data = res;
                  title = data.title;
                  content = data.body;
                  console.log(title, data, data.category);
                  categories.forEach(category => {
                    if(data.category === category.category) {
                      selected_category = category;
                    }
                  })
                }
            }).catch(err => {
                console.log(err);
            });
    }

    if(params.content_id !== "") {
      get_data(params.content_id);
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
        <select class="input_category" bind:value={selected_category} on:change={() => {console.log(selected_category);}}>
          {#each categories as category}
            <option value={category}>
              {category.text}
            </option>
          {/each}
        </select>
      </label>
      <textarea class="content" bind:value={content}></textarea>
      {#if params.content_id === ""}
        <div class="input_element">
          <label>
            사진 및 파일:
            <input type="file" multiple on:change={handleUpload} />
          </label>
        </div>
      {/if}
      <button class="submit">{params.content_id === "" ? "글 쓰기" : "수정하기"}</button>
    </form>
</div>