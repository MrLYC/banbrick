(function(){
    var gh_api = null;
    var toc_tpl = null;
    var md_converter = null;
    var toc_map = null;
    
    var $toc_list = null;
    var $article_area = null;
    var $title = null;

    function render_toc(toc){
        toc_map = {};
        
        for(var i in toc){
            var item = toc[i];
            toc_map[item.sha] = item;
        }
        
        $toc_list.html(toc_tpl({
            toclist: toc
        }));
        
        $(".toc-lnk").click(function(argument) {
            var self = $(this);
            var sha = self.data("sha");
            var item = toc_map[sha];
            active_item(item);
        })
    }
    
    function render_markdown(text) {
        $article_area.html(md_converter.makeHtml(text));
        var $pre_area = $article_area.find("pre");
        $pre_area.addClass("hljs");
        $pre_area.find("code").each(function(i, block) {
            hljs.highlightBlock(block);
        });
        $article_area.find("h1, h2, h3, h4, h5").each(function() {
            var self = $(this);
            self.attr("id", escape(self.text()));
        });
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
                    if(item.type == "file" && item.name.endsWith(".md")){
                        toc_list.push({
                            name: item["name"],
                            url: item["download_url"],
                            type: item["type"],
                            size: item["size"],
                            path: item["path"],
                            sha: item["sha"],
                        });
                    }
                }
                toc_list.sort(function(a, b) {
                    return a > b;
                })
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
        fetch_doc(item);
        $(".active-toc-item").removeClass("active-toc-item");
        $("#toc_item_" + item.sha).addClass("active-toc-item");
        $("#content").scrollTop(0);
    }
    
    $(function init(){
        gh_api = [META.api, "repos", META.user, META.repo, "contents"].join("/");
        toc_tpl = Handlebars.compile($("#toc-tpl").html());
        md_converter = new showdown.Converter();
    
        $toc_list = $("#toc-list");
        $article_area = $("#article");
        $title = $("title");
        
        hljs.initHighlightingOnLoad();
    
        render_markdown($("#md-default").text());
        list_dir(META.directory, function(data) {
            var selected = document.location.hash.substr(1);
            var active_toc_item = null;
            for(var i in data){
                var item = data[i];
                if(item.name == META.default){
                    data.splice(i, 1);
                    data.splice(0, 0, item);
                    if(selected.length == 0){
                        active_toc_item = item;
                        break;
                    }
                }
                if(selected.length > 1 && item.name == selected){
                    active_toc_item = item;
                }
            }
            
            render_toc(data);
            if(active_toc_item != null){
                $(".toc-lnk[data-sha=" + active_toc_item.sha + "]").click();
            }
        });
    });
})();