(function(){
  const s=document.getElementById('filmy'); if(!s) return;
  const player=s.querySelector('[data-player]');
  let current='8H4GNjbGqLw';
  function play(id){
    player.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0" title="Film ADJ" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
  }
  player.addEventListener('click',e=>{ if(e.target.closest('[data-facade]')) play(current); });
  s.querySelectorAll('.vf__item').forEach(b=>b.addEventListener('click',()=>{
    s.querySelectorAll('.vf__item').forEach(x=>{x.classList.remove('is-active');x.setAttribute('aria-pressed','false')});
    b.classList.add('is-active'); b.setAttribute('aria-pressed','true');
    current=b.dataset.id; play(current);
  }));
})();
