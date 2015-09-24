(function(){
    var gh_api = null;
    var toc_tpl = null;
    var md_converter = null;
    var doc_list = null;
    var dir_list = null;
    var active_toc_item= null;
    
    var $toc_list = null;
    var $article_area = null;
    var $title = null;

    function render_toc(toc){
        $toc_list.html(toc_tpl({
            toclist: toc
        }));
    }
    
    function render_markdown(text) {
        $article_area.html(md_converter.makeHtml(text));
    }
    
    function list_dir(dir_name, callback) {
        if(typeof dir_name == "undefined"){
            dir_name = META.directory;
        }
        var url = gh_api + "/" + dir_name;
        $.getJSON(
            url, function(data){
                var toc_list = [];
                for(var i in data){
                    var item = data[i];
                    toc_list.push({
                        name: item["name"],
                        url: item["download_url"],
                        type: item["type"],
                        size: item["size"],
                        path: item["path"],
                        sha: item["sha"],
                    });
                }
                callback(toc_list);
            }
        );
    }
    
    function fetch_doc(item){
        $.get(item.url, function(data) {
            render_markdown(data);
            var $h1 = $("#article > h1:eq(0)");
            if($h1.length > 0){
                $title.text($h1.text());
            }
        });
        $title.text(item.name);
    }
    
    function active_item(item) {
        $(".active-toc-item").removeClass("active-toc-item");
        $("#toc_item_" + item.sha).addClass("active-toc-item");
    }
    
    $(function init(){
        gh_api = [META.api, "repos", META.user, META.repo, "contents"].join("/");
        toc_tpl = Handlebars.compile($("#toc-tpl").html());
        md_converter = new showdown.Converter();
    
        $toc_list = $("#toc-list");
        $article_area = $("#article");
        $title = $("title");
    
        render_markdown($("#md-default").text());
        list_dir(META.directory, function(data) {
            dir_list = data;
            doc_list = [];
            for(var i in data){
                var item = data[i];
                if(item.name == META.default){
                    fetch_doc(item);
                    active_toc_item = item;
                }
                if(item.type == "file" && item.name.endsWith(".md")){
                    doc_list.push(item);
                }
            }
            render_toc(doc_list);
            active_item(active_toc_item);
        });
    });
})();