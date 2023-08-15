<script lang="ts">
    import "./SubPage_Write.scss";

    let title = '';
    let content = [];
    let youtubeLink = '';

    let imageFile;
    let imageUrl;

    function handleSubmit() {
        console.log("Title:", title);
        console.log("Content:", content);
        console.log("YouTube Link:", youtubeLink);
        console.log("Image URL:", imageUrl);
    }

    function handleImageUpload(event) {
        imageFile = event.target.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
        imageUrl = e.target.result;
        };

        reader.readAsDataURL(imageFile);
    }

    function addImageToContent() {
        if (imageUrl) {
        content = [...content, { type: 'image', src: imageUrl }];
        imageFile = null;
        imageUrl = '';
        }
    }
</script>

<div class="container_write">
    <h1>글 쓰기</h1>
    <form class="form" on:submit|preventDefault={handleSubmit}>
      <label>
        제목:
        <input bind:value={title} />
      </label>
      <textarea class="content" bind:value={content}></textarea>
      <div class="input_element">
        <label>
          Image:
          <input type="file" accept="image/*" on:change={handleImageUpload} />
          <button type="button" on:click={addImageToContent}>Add Image to Content</button>
        </label>
      </div>
      <button type="submit">Submit</button>
    </form>
  
    {#each content as item, index (index)}
      {#if item.type === 'image'}
        <img src={item.src} alt={`Image ${index}`} style="max-width: 100%; height: auto;" />
      {:else if item.type === 'text'}
        <p>{item.text}</p>
      {/if}
    {/each}
</div>