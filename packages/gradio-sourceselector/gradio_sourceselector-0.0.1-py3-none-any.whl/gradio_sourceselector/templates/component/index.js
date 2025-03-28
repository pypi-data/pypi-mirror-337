const {
  SvelteComponent: El,
  assign: kl,
  create_slot: Al,
  detach: yl,
  element: $l,
  get_all_dirty_from_scope: Ll,
  get_slot_changes: ql,
  get_spread_update: Rl,
  init: Ol,
  insert: Nl,
  safe_not_equal: Dl,
  set_dynamic_element_data: Yn,
  set_style: te,
  toggle_class: Te,
  transition_in: Yo,
  transition_out: jo,
  update_slot_base: Ml
} = window.__gradio__svelte__internal;
function Il(n) {
  let e, t, o;
  const l = (
    /*#slots*/
    n[18].default
  ), i = Al(
    l,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let s = 0; s < a.length; s += 1)
    r = kl(r, a[s]);
  return {
    c() {
      e = $l(
        /*tag*/
        n[14]
      ), i && i.c(), Yn(
        /*tag*/
        n[14]
      )(e, r), Te(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), Te(
        e,
        "padded",
        /*padding*/
        n[6]
      ), Te(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), Te(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), Te(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), te(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), te(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), te(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), te(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), te(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), te(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), te(e, "border-width", "var(--block-border-width)");
    },
    m(s, _) {
      Nl(s, e, _), i && i.m(e, null), o = !0;
    },
    p(s, _) {
      i && i.p && (!o || _ & /*$$scope*/
      131072) && Ml(
        i,
        l,
        s,
        /*$$scope*/
        s[17],
        o ? ql(
          l,
          /*$$scope*/
          s[17],
          _,
          null
        ) : Ll(
          /*$$scope*/
          s[17]
        ),
        null
      ), Yn(
        /*tag*/
        s[14]
      )(e, r = Rl(a, [
        (!o || _ & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!o || _ & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!o || _ & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), Te(
        e,
        "hidden",
        /*visible*/
        s[10] === !1
      ), Te(
        e,
        "padded",
        /*padding*/
        s[6]
      ), Te(
        e,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), Te(
        e,
        "border_contrast",
        /*border_mode*/
        s[5] === "contrast"
      ), Te(e, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), _ & /*height*/
      1 && te(
        e,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), _ & /*width*/
      2 && te(e, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), _ & /*variant*/
      16 && te(
        e,
        "border-style",
        /*variant*/
        s[4]
      ), _ & /*allow_overflow*/
      2048 && te(
        e,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), _ & /*scale*/
      4096 && te(
        e,
        "flex-grow",
        /*scale*/
        s[12]
      ), _ & /*min_width*/
      8192 && te(e, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      o || (Yo(i, s), o = !0);
    },
    o(s) {
      jo(i, s), o = !1;
    },
    d(s) {
      s && yl(e), i && i.d(s);
    }
  };
}
function Pl(n) {
  let e, t = (
    /*tag*/
    n[14] && Il(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(o, l) {
      t && t.m(o, l), e = !0;
    },
    p(o, [l]) {
      /*tag*/
      o[14] && t.p(o, l);
    },
    i(o) {
      e || (Yo(t, o), e = !0);
    },
    o(o) {
      jo(t, o), e = !1;
    },
    d(o) {
      t && t.d(o);
    }
  };
}
function Fl(n, e, t) {
  let { $$slots: o = {}, $$scope: l } = e, { height: i = void 0 } = e, { width: a = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: s = [] } = e, { variant: _ = "solid" } = e, { border_mode: c = "base" } = e, { padding: d = !0 } = e, { type: h = "normal" } = e, { test_id: b = void 0 } = e, { explicit_call: S = !1 } = e, { container: E = !0 } = e, { visible: A = !0 } = e, { allow_overflow: q = !0 } = e, { scale: g = null } = e, { min_width: m = 0 } = e, p = h === "fieldset" ? "fieldset" : "div";
  const y = (w) => {
    if (w !== void 0) {
      if (typeof w == "number")
        return w + "px";
      if (typeof w == "string")
        return w;
    }
  };
  return n.$$set = (w) => {
    "height" in w && t(0, i = w.height), "width" in w && t(1, a = w.width), "elem_id" in w && t(2, r = w.elem_id), "elem_classes" in w && t(3, s = w.elem_classes), "variant" in w && t(4, _ = w.variant), "border_mode" in w && t(5, c = w.border_mode), "padding" in w && t(6, d = w.padding), "type" in w && t(16, h = w.type), "test_id" in w && t(7, b = w.test_id), "explicit_call" in w && t(8, S = w.explicit_call), "container" in w && t(9, E = w.container), "visible" in w && t(10, A = w.visible), "allow_overflow" in w && t(11, q = w.allow_overflow), "scale" in w && t(12, g = w.scale), "min_width" in w && t(13, m = w.min_width), "$$scope" in w && t(17, l = w.$$scope);
  }, [
    i,
    a,
    r,
    s,
    _,
    c,
    d,
    b,
    S,
    E,
    A,
    q,
    g,
    m,
    p,
    y,
    h,
    l,
    o
  ];
}
class Ul extends El {
  constructor(e) {
    super(), Ol(this, e, Fl, Pl, Dl, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: zl,
  attr: Hl,
  create_slot: Bl,
  detach: Gl,
  element: Wl,
  get_all_dirty_from_scope: Vl,
  get_slot_changes: Yl,
  init: jl,
  insert: Xl,
  safe_not_equal: Zl,
  transition_in: Kl,
  transition_out: Jl,
  update_slot_base: Ql
} = window.__gradio__svelte__internal;
function xl(n) {
  let e, t;
  const o = (
    /*#slots*/
    n[1].default
  ), l = Bl(
    o,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = Wl("div"), l && l.c(), Hl(e, "class", "svelte-1hnfib2");
    },
    m(i, a) {
      Xl(i, e, a), l && l.m(e, null), t = !0;
    },
    p(i, [a]) {
      l && l.p && (!t || a & /*$$scope*/
      1) && Ql(
        l,
        o,
        i,
        /*$$scope*/
        i[0],
        t ? Yl(
          o,
          /*$$scope*/
          i[0],
          a,
          null
        ) : Vl(
          /*$$scope*/
          i[0]
        ),
        null
      );
    },
    i(i) {
      t || (Kl(l, i), t = !0);
    },
    o(i) {
      Jl(l, i), t = !1;
    },
    d(i) {
      i && Gl(e), l && l.d(i);
    }
  };
}
function ei(n, e, t) {
  let { $$slots: o = {}, $$scope: l } = e;
  return n.$$set = (i) => {
    "$$scope" in i && t(0, l = i.$$scope);
  }, [l, o];
}
class ti extends zl {
  constructor(e) {
    super(), jl(this, e, ei, xl, Zl, {});
  }
}
const {
  SvelteComponent: ni,
  attr: jn,
  check_outros: oi,
  create_component: li,
  create_slot: ii,
  destroy_component: ai,
  detach: Ft,
  element: si,
  empty: ri,
  get_all_dirty_from_scope: _i,
  get_slot_changes: fi,
  group_outros: ci,
  init: ui,
  insert: Ut,
  mount_component: di,
  safe_not_equal: mi,
  set_data: pi,
  space: gi,
  text: hi,
  toggle_class: nt,
  transition_in: Tt,
  transition_out: zt,
  update_slot_base: bi
} = window.__gradio__svelte__internal;
function Xn(n) {
  let e, t;
  return e = new ti({
    props: {
      $$slots: { default: [vi] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      li(e.$$.fragment);
    },
    m(o, l) {
      di(e, o, l), t = !0;
    },
    p(o, l) {
      const i = {};
      l & /*$$scope, info*/
      10 && (i.$$scope = { dirty: l, ctx: o }), e.$set(i);
    },
    i(o) {
      t || (Tt(e.$$.fragment, o), t = !0);
    },
    o(o) {
      zt(e.$$.fragment, o), t = !1;
    },
    d(o) {
      ai(e, o);
    }
  };
}
function vi(n) {
  let e;
  return {
    c() {
      e = hi(
        /*info*/
        n[1]
      );
    },
    m(t, o) {
      Ut(t, e, o);
    },
    p(t, o) {
      o & /*info*/
      2 && pi(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Ft(e);
    }
  };
}
function wi(n) {
  let e, t, o, l;
  const i = (
    /*#slots*/
    n[2].default
  ), a = ii(
    i,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let r = (
    /*info*/
    n[1] && Xn(n)
  );
  return {
    c() {
      e = si("span"), a && a.c(), t = gi(), r && r.c(), o = ri(), jn(e, "data-testid", "block-info"), jn(e, "class", "svelte-22c38v"), nt(e, "sr-only", !/*show_label*/
      n[0]), nt(e, "hide", !/*show_label*/
      n[0]), nt(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(s, _) {
      Ut(s, e, _), a && a.m(e, null), Ut(s, t, _), r && r.m(s, _), Ut(s, o, _), l = !0;
    },
    p(s, [_]) {
      a && a.p && (!l || _ & /*$$scope*/
      8) && bi(
        a,
        i,
        s,
        /*$$scope*/
        s[3],
        l ? fi(
          i,
          /*$$scope*/
          s[3],
          _,
          null
        ) : _i(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!l || _ & /*show_label*/
      1) && nt(e, "sr-only", !/*show_label*/
      s[0]), (!l || _ & /*show_label*/
      1) && nt(e, "hide", !/*show_label*/
      s[0]), (!l || _ & /*info*/
      2) && nt(
        e,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? r ? (r.p(s, _), _ & /*info*/
      2 && Tt(r, 1)) : (r = Xn(s), r.c(), Tt(r, 1), r.m(o.parentNode, o)) : r && (ci(), zt(r, 1, 1, () => {
        r = null;
      }), oi());
    },
    i(s) {
      l || (Tt(a, s), Tt(r), l = !0);
    },
    o(s) {
      zt(a, s), zt(r), l = !1;
    },
    d(s) {
      s && (Ft(e), Ft(t), Ft(o)), a && a.d(s), r && r.d(s);
    }
  };
}
function Si(n, e, t) {
  let { $$slots: o = {}, $$scope: l } = e, { show_label: i = !0 } = e, { info: a = void 0 } = e;
  return n.$$set = (r) => {
    "show_label" in r && t(0, i = r.show_label), "info" in r && t(1, a = r.info), "$$scope" in r && t(3, l = r.$$scope);
  }, [i, a, o, l];
}
class Ti extends ni {
  constructor(e) {
    super(), ui(this, e, Si, wi, mi, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: ir,
  append: ar,
  attr: sr,
  create_component: rr,
  destroy_component: _r,
  detach: fr,
  element: cr,
  init: ur,
  insert: dr,
  mount_component: mr,
  safe_not_equal: pr,
  set_data: gr,
  space: hr,
  text: br,
  toggle_class: vr,
  transition_in: wr,
  transition_out: Sr
} = window.__gradio__svelte__internal, {
  SvelteComponent: Ci,
  append: dn,
  attr: Re,
  bubble: Ei,
  create_component: ki,
  destroy_component: Ai,
  detach: Xo,
  element: mn,
  init: yi,
  insert: Zo,
  listen: $i,
  mount_component: Li,
  safe_not_equal: qi,
  set_data: Ri,
  set_style: ot,
  space: Oi,
  text: Ni,
  toggle_class: x,
  transition_in: Di,
  transition_out: Mi
} = window.__gradio__svelte__internal;
function Zn(n) {
  let e, t;
  return {
    c() {
      e = mn("span"), t = Ni(
        /*label*/
        n[1]
      ), Re(e, "class", "svelte-1lrphxw");
    },
    m(o, l) {
      Zo(o, e, l), dn(e, t);
    },
    p(o, l) {
      l & /*label*/
      2 && Ri(
        t,
        /*label*/
        o[1]
      );
    },
    d(o) {
      o && Xo(e);
    }
  };
}
function Ii(n) {
  let e, t, o, l, i, a, r, s = (
    /*show_label*/
    n[2] && Zn(n)
  );
  return l = new /*Icon*/
  n[0]({}), {
    c() {
      e = mn("button"), s && s.c(), t = Oi(), o = mn("div"), ki(l.$$.fragment), Re(o, "class", "svelte-1lrphxw"), x(
        o,
        "small",
        /*size*/
        n[4] === "small"
      ), x(
        o,
        "large",
        /*size*/
        n[4] === "large"
      ), x(
        o,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], Re(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), Re(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), Re(
        e,
        "title",
        /*label*/
        n[1]
      ), Re(e, "class", "svelte-1lrphxw"), x(
        e,
        "pending",
        /*pending*/
        n[3]
      ), x(
        e,
        "padded",
        /*padded*/
        n[5]
      ), x(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), x(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), ot(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), ot(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), ot(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(_, c) {
      Zo(_, e, c), s && s.m(e, null), dn(e, t), dn(e, o), Li(l, o, null), i = !0, a || (r = $i(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), a = !0);
    },
    p(_, [c]) {
      /*show_label*/
      _[2] ? s ? s.p(_, c) : (s = Zn(_), s.c(), s.m(e, t)) : s && (s.d(1), s = null), (!i || c & /*size*/
      16) && x(
        o,
        "small",
        /*size*/
        _[4] === "small"
      ), (!i || c & /*size*/
      16) && x(
        o,
        "large",
        /*size*/
        _[4] === "large"
      ), (!i || c & /*size*/
      16) && x(
        o,
        "medium",
        /*size*/
        _[4] === "medium"
      ), (!i || c & /*disabled*/
      128) && (e.disabled = /*disabled*/
      _[7]), (!i || c & /*label*/
      2) && Re(
        e,
        "aria-label",
        /*label*/
        _[1]
      ), (!i || c & /*hasPopup*/
      256) && Re(
        e,
        "aria-haspopup",
        /*hasPopup*/
        _[8]
      ), (!i || c & /*label*/
      2) && Re(
        e,
        "title",
        /*label*/
        _[1]
      ), (!i || c & /*pending*/
      8) && x(
        e,
        "pending",
        /*pending*/
        _[3]
      ), (!i || c & /*padded*/
      32) && x(
        e,
        "padded",
        /*padded*/
        _[5]
      ), (!i || c & /*highlight*/
      64) && x(
        e,
        "highlight",
        /*highlight*/
        _[6]
      ), (!i || c & /*transparent*/
      512) && x(
        e,
        "transparent",
        /*transparent*/
        _[9]
      ), c & /*disabled, _color*/
      4224 && ot(e, "color", !/*disabled*/
      _[7] && /*_color*/
      _[12] ? (
        /*_color*/
        _[12]
      ) : "var(--block-label-text-color)"), c & /*disabled, background*/
      1152 && ot(e, "--bg-color", /*disabled*/
      _[7] ? "auto" : (
        /*background*/
        _[10]
      )), c & /*offset*/
      2048 && ot(
        e,
        "margin-left",
        /*offset*/
        _[11] + "px"
      );
    },
    i(_) {
      i || (Di(l.$$.fragment, _), i = !0);
    },
    o(_) {
      Mi(l.$$.fragment, _), i = !1;
    },
    d(_) {
      _ && Xo(e), s && s.d(), Ai(l), a = !1, r();
    }
  };
}
function Pi(n, e, t) {
  let o, { Icon: l } = e, { label: i = "" } = e, { show_label: a = !1 } = e, { pending: r = !1 } = e, { size: s = "small" } = e, { padded: _ = !0 } = e, { highlight: c = !1 } = e, { disabled: d = !1 } = e, { hasPopup: h = !1 } = e, { color: b = "var(--block-label-text-color)" } = e, { transparent: S = !1 } = e, { background: E = "var(--background-fill-primary)" } = e, { offset: A = 0 } = e;
  function q(g) {
    Ei.call(this, n, g);
  }
  return n.$$set = (g) => {
    "Icon" in g && t(0, l = g.Icon), "label" in g && t(1, i = g.label), "show_label" in g && t(2, a = g.show_label), "pending" in g && t(3, r = g.pending), "size" in g && t(4, s = g.size), "padded" in g && t(5, _ = g.padded), "highlight" in g && t(6, c = g.highlight), "disabled" in g && t(7, d = g.disabled), "hasPopup" in g && t(8, h = g.hasPopup), "color" in g && t(13, b = g.color), "transparent" in g && t(9, S = g.transparent), "background" in g && t(10, E = g.background), "offset" in g && t(11, A = g.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, o = c ? "var(--color-accent)" : b);
  }, [
    l,
    i,
    a,
    r,
    s,
    _,
    c,
    d,
    h,
    S,
    E,
    A,
    o,
    b,
    q
  ];
}
class Fi extends Ci {
  constructor(e) {
    super(), yi(this, e, Pi, Ii, qi, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: Tr,
  append: Cr,
  attr: Er,
  binding_callbacks: kr,
  create_slot: Ar,
  detach: yr,
  element: $r,
  get_all_dirty_from_scope: Lr,
  get_slot_changes: qr,
  init: Rr,
  insert: Or,
  safe_not_equal: Nr,
  toggle_class: Dr,
  transition_in: Mr,
  transition_out: Ir,
  update_slot_base: Pr
} = window.__gradio__svelte__internal, {
  SvelteComponent: Fr,
  append: Ur,
  attr: zr,
  detach: Hr,
  init: Br,
  insert: Gr,
  noop: Wr,
  safe_not_equal: Vr,
  svg_element: Yr
} = window.__gradio__svelte__internal, {
  SvelteComponent: jr,
  append: Xr,
  attr: Zr,
  detach: Kr,
  init: Jr,
  insert: Qr,
  noop: xr,
  safe_not_equal: e_,
  svg_element: t_
} = window.__gradio__svelte__internal, {
  SvelteComponent: n_,
  append: o_,
  attr: l_,
  detach: i_,
  init: a_,
  insert: s_,
  noop: r_,
  safe_not_equal: __,
  svg_element: f_
} = window.__gradio__svelte__internal, {
  SvelteComponent: c_,
  append: u_,
  attr: d_,
  detach: m_,
  init: p_,
  insert: g_,
  noop: h_,
  safe_not_equal: b_,
  svg_element: v_
} = window.__gradio__svelte__internal, {
  SvelteComponent: w_,
  append: S_,
  attr: T_,
  detach: C_,
  init: E_,
  insert: k_,
  noop: A_,
  safe_not_equal: y_,
  svg_element: $_
} = window.__gradio__svelte__internal, {
  SvelteComponent: L_,
  append: q_,
  attr: R_,
  detach: O_,
  init: N_,
  insert: D_,
  noop: M_,
  safe_not_equal: I_,
  svg_element: P_
} = window.__gradio__svelte__internal, {
  SvelteComponent: F_,
  append: U_,
  attr: z_,
  detach: H_,
  init: B_,
  insert: G_,
  noop: W_,
  safe_not_equal: V_,
  svg_element: Y_
} = window.__gradio__svelte__internal, {
  SvelteComponent: j_,
  append: X_,
  attr: Z_,
  detach: K_,
  init: J_,
  insert: Q_,
  noop: x_,
  safe_not_equal: ef,
  svg_element: tf
} = window.__gradio__svelte__internal, {
  SvelteComponent: nf,
  append: of,
  attr: lf,
  detach: af,
  init: sf,
  insert: rf,
  noop: _f,
  safe_not_equal: ff,
  svg_element: cf
} = window.__gradio__svelte__internal, {
  SvelteComponent: uf,
  append: df,
  attr: mf,
  detach: pf,
  init: gf,
  insert: hf,
  noop: bf,
  safe_not_equal: vf,
  svg_element: wf
} = window.__gradio__svelte__internal, {
  SvelteComponent: Ui,
  append: en,
  attr: me,
  detach: zi,
  init: Hi,
  insert: Bi,
  noop: tn,
  safe_not_equal: Gi,
  set_style: Ce,
  svg_element: Ot
} = window.__gradio__svelte__internal;
function Wi(n) {
  let e, t, o, l;
  return {
    c() {
      e = Ot("svg"), t = Ot("g"), o = Ot("path"), l = Ot("path"), me(o, "d", "M18,6L6.087,17.913"), Ce(o, "fill", "none"), Ce(o, "fill-rule", "nonzero"), Ce(o, "stroke-width", "2px"), me(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), me(l, "d", "M4.364,4.364L19.636,19.636"), Ce(l, "fill", "none"), Ce(l, "fill-rule", "nonzero"), Ce(l, "stroke-width", "2px"), me(e, "width", "100%"), me(e, "height", "100%"), me(e, "viewBox", "0 0 24 24"), me(e, "version", "1.1"), me(e, "xmlns", "http://www.w3.org/2000/svg"), me(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), me(e, "xml:space", "preserve"), me(e, "stroke", "currentColor"), Ce(e, "fill-rule", "evenodd"), Ce(e, "clip-rule", "evenodd"), Ce(e, "stroke-linecap", "round"), Ce(e, "stroke-linejoin", "round");
    },
    m(i, a) {
      Bi(i, e, a), en(e, t), en(t, o), en(e, l);
    },
    p: tn,
    i: tn,
    o: tn,
    d(i) {
      i && zi(e);
    }
  };
}
class Vi extends Ui {
  constructor(e) {
    super(), Hi(this, e, null, Wi, Gi, {});
  }
}
const {
  SvelteComponent: Sf,
  append: Tf,
  attr: Cf,
  detach: Ef,
  init: kf,
  insert: Af,
  noop: yf,
  safe_not_equal: $f,
  svg_element: Lf
} = window.__gradio__svelte__internal, {
  SvelteComponent: qf,
  append: Rf,
  attr: Of,
  detach: Nf,
  init: Df,
  insert: Mf,
  noop: If,
  safe_not_equal: Pf,
  svg_element: Ff
} = window.__gradio__svelte__internal, {
  SvelteComponent: Uf,
  append: zf,
  attr: Hf,
  detach: Bf,
  init: Gf,
  insert: Wf,
  noop: Vf,
  safe_not_equal: Yf,
  svg_element: jf
} = window.__gradio__svelte__internal, {
  SvelteComponent: Xf,
  append: Zf,
  attr: Kf,
  detach: Jf,
  init: Qf,
  insert: xf,
  noop: ec,
  safe_not_equal: tc,
  svg_element: nc
} = window.__gradio__svelte__internal, {
  SvelteComponent: oc,
  append: lc,
  attr: ic,
  detach: ac,
  init: sc,
  insert: rc,
  noop: _c,
  safe_not_equal: fc,
  svg_element: cc
} = window.__gradio__svelte__internal, {
  SvelteComponent: uc,
  append: dc,
  attr: mc,
  detach: pc,
  init: gc,
  insert: hc,
  noop: bc,
  safe_not_equal: vc,
  svg_element: wc
} = window.__gradio__svelte__internal, {
  SvelteComponent: Yi,
  append: ji,
  attr: lt,
  detach: Xi,
  init: Zi,
  insert: Ki,
  noop: nn,
  safe_not_equal: Ji,
  svg_element: Kn
} = window.__gradio__svelte__internal;
function Qi(n) {
  let e, t;
  return {
    c() {
      e = Kn("svg"), t = Kn("path"), lt(t, "d", "M5 8l4 4 4-4z"), lt(e, "class", "dropdown-arrow svelte-145leq6"), lt(e, "xmlns", "http://www.w3.org/2000/svg"), lt(e, "width", "100%"), lt(e, "height", "100%"), lt(e, "viewBox", "0 0 18 18");
    },
    m(o, l) {
      Ki(o, e, l), ji(e, t);
    },
    p: nn,
    i: nn,
    o: nn,
    d(o) {
      o && Xi(e);
    }
  };
}
class xi extends Yi {
  constructor(e) {
    super(), Zi(this, e, null, Qi, Ji, {});
  }
}
const {
  SvelteComponent: Sc,
  append: Tc,
  attr: Cc,
  detach: Ec,
  init: kc,
  insert: Ac,
  noop: yc,
  safe_not_equal: $c,
  svg_element: Lc
} = window.__gradio__svelte__internal, {
  SvelteComponent: qc,
  append: Rc,
  attr: Oc,
  detach: Nc,
  init: Dc,
  insert: Mc,
  noop: Ic,
  safe_not_equal: Pc,
  svg_element: Fc
} = window.__gradio__svelte__internal, {
  SvelteComponent: Uc,
  append: zc,
  attr: Hc,
  detach: Bc,
  init: Gc,
  insert: Wc,
  noop: Vc,
  safe_not_equal: Yc,
  svg_element: jc
} = window.__gradio__svelte__internal, {
  SvelteComponent: Xc,
  append: Zc,
  attr: Kc,
  detach: Jc,
  init: Qc,
  insert: xc,
  noop: eu,
  safe_not_equal: tu,
  svg_element: nu
} = window.__gradio__svelte__internal, {
  SvelteComponent: ou,
  append: lu,
  attr: iu,
  detach: au,
  init: su,
  insert: ru,
  noop: _u,
  safe_not_equal: fu,
  svg_element: cu
} = window.__gradio__svelte__internal, {
  SvelteComponent: uu,
  append: du,
  attr: mu,
  detach: pu,
  init: gu,
  insert: hu,
  noop: bu,
  safe_not_equal: vu,
  svg_element: wu
} = window.__gradio__svelte__internal, {
  SvelteComponent: Su,
  append: Tu,
  attr: Cu,
  detach: Eu,
  init: ku,
  insert: Au,
  noop: yu,
  safe_not_equal: $u,
  svg_element: Lu
} = window.__gradio__svelte__internal, {
  SvelteComponent: qu,
  append: Ru,
  attr: Ou,
  detach: Nu,
  init: Du,
  insert: Mu,
  noop: Iu,
  safe_not_equal: Pu,
  svg_element: Fu
} = window.__gradio__svelte__internal, {
  SvelteComponent: Uu,
  append: zu,
  attr: Hu,
  detach: Bu,
  init: Gu,
  insert: Wu,
  noop: Vu,
  safe_not_equal: Yu,
  svg_element: ju
} = window.__gradio__svelte__internal, {
  SvelteComponent: Xu,
  append: Zu,
  attr: Ku,
  detach: Ju,
  init: Qu,
  insert: xu,
  noop: ed,
  safe_not_equal: td,
  svg_element: nd
} = window.__gradio__svelte__internal, {
  SvelteComponent: od,
  append: ld,
  attr: id,
  detach: ad,
  init: sd,
  insert: rd,
  noop: _d,
  safe_not_equal: fd,
  svg_element: cd
} = window.__gradio__svelte__internal, {
  SvelteComponent: ud,
  append: dd,
  attr: md,
  detach: pd,
  init: gd,
  insert: hd,
  noop: bd,
  safe_not_equal: vd,
  svg_element: wd
} = window.__gradio__svelte__internal, {
  SvelteComponent: Sd,
  append: Td,
  attr: Cd,
  detach: Ed,
  init: kd,
  insert: Ad,
  noop: yd,
  safe_not_equal: $d,
  svg_element: Ld
} = window.__gradio__svelte__internal, {
  SvelteComponent: qd,
  append: Rd,
  attr: Od,
  detach: Nd,
  init: Dd,
  insert: Md,
  noop: Id,
  safe_not_equal: Pd,
  svg_element: Fd
} = window.__gradio__svelte__internal, {
  SvelteComponent: Ud,
  append: zd,
  attr: Hd,
  detach: Bd,
  init: Gd,
  insert: Wd,
  noop: Vd,
  safe_not_equal: Yd,
  svg_element: jd
} = window.__gradio__svelte__internal, {
  SvelteComponent: Xd,
  append: Zd,
  attr: Kd,
  detach: Jd,
  init: Qd,
  insert: xd,
  noop: em,
  safe_not_equal: tm,
  svg_element: nm
} = window.__gradio__svelte__internal, {
  SvelteComponent: om,
  append: lm,
  attr: im,
  detach: am,
  init: sm,
  insert: rm,
  noop: _m,
  safe_not_equal: fm,
  svg_element: cm
} = window.__gradio__svelte__internal, {
  SvelteComponent: um,
  append: dm,
  attr: mm,
  detach: pm,
  init: gm,
  insert: hm,
  noop: bm,
  safe_not_equal: vm,
  svg_element: wm
} = window.__gradio__svelte__internal, {
  SvelteComponent: Sm,
  append: Tm,
  attr: Cm,
  detach: Em,
  init: km,
  insert: Am,
  noop: ym,
  safe_not_equal: $m,
  svg_element: Lm
} = window.__gradio__svelte__internal, {
  SvelteComponent: qm,
  append: Rm,
  attr: Om,
  detach: Nm,
  init: Dm,
  insert: Mm,
  noop: Im,
  safe_not_equal: Pm,
  svg_element: Fm
} = window.__gradio__svelte__internal, {
  SvelteComponent: Um,
  append: zm,
  attr: Hm,
  detach: Bm,
  init: Gm,
  insert: Wm,
  noop: Vm,
  safe_not_equal: Ym,
  set_style: jm,
  svg_element: Xm
} = window.__gradio__svelte__internal, {
  SvelteComponent: ea,
  append: ta,
  attr: on,
  detach: na,
  init: oa,
  insert: la,
  noop: ln,
  safe_not_equal: ia,
  svg_element: Jn
} = window.__gradio__svelte__internal;
function aa(n) {
  let e, t;
  return {
    c() {
      e = Jn("svg"), t = Jn("path"), on(t, "d", "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"), on(e, "xmlns", "http://www.w3.org/2000/svg"), on(e, "viewBox", "0 0 24 24");
    },
    m(o, l) {
      la(o, e, l), ta(e, t);
    },
    p: ln,
    i: ln,
    o: ln,
    d(o) {
      o && na(e);
    }
  };
}
class sa extends ea {
  constructor(e) {
    super(), oa(this, e, null, aa, ia, {});
  }
}
const {
  SvelteComponent: Zm,
  append: Km,
  attr: Jm,
  detach: Qm,
  init: xm,
  insert: e0,
  noop: t0,
  safe_not_equal: n0,
  svg_element: o0
} = window.__gradio__svelte__internal, {
  SvelteComponent: l0,
  append: i0,
  attr: a0,
  detach: s0,
  init: r0,
  insert: _0,
  noop: f0,
  safe_not_equal: c0,
  svg_element: u0
} = window.__gradio__svelte__internal, {
  SvelteComponent: d0,
  append: m0,
  attr: p0,
  detach: g0,
  init: h0,
  insert: b0,
  noop: v0,
  safe_not_equal: w0,
  svg_element: S0
} = window.__gradio__svelte__internal, {
  SvelteComponent: T0,
  append: C0,
  attr: E0,
  detach: k0,
  init: A0,
  insert: y0,
  noop: $0,
  safe_not_equal: L0,
  svg_element: q0
} = window.__gradio__svelte__internal, {
  SvelteComponent: R0,
  append: O0,
  attr: N0,
  detach: D0,
  init: M0,
  insert: I0,
  noop: P0,
  safe_not_equal: F0,
  svg_element: U0
} = window.__gradio__svelte__internal, {
  SvelteComponent: z0,
  append: H0,
  attr: B0,
  detach: G0,
  init: W0,
  insert: V0,
  noop: Y0,
  safe_not_equal: j0,
  svg_element: X0
} = window.__gradio__svelte__internal, {
  SvelteComponent: Z0,
  append: K0,
  attr: J0,
  detach: Q0,
  init: x0,
  insert: ep,
  noop: tp,
  safe_not_equal: np,
  svg_element: op
} = window.__gradio__svelte__internal, {
  SvelteComponent: lp,
  append: ip,
  attr: ap,
  detach: sp,
  init: rp,
  insert: _p,
  noop: fp,
  safe_not_equal: cp,
  svg_element: up,
  text: dp
} = window.__gradio__svelte__internal, {
  SvelteComponent: mp,
  append: pp,
  attr: gp,
  detach: hp,
  init: bp,
  insert: vp,
  noop: wp,
  safe_not_equal: Sp,
  svg_element: Tp
} = window.__gradio__svelte__internal, {
  SvelteComponent: Cp,
  append: Ep,
  attr: kp,
  detach: Ap,
  init: yp,
  insert: $p,
  noop: Lp,
  safe_not_equal: qp,
  svg_element: Rp
} = window.__gradio__svelte__internal, {
  SvelteComponent: Op,
  append: Np,
  attr: Dp,
  detach: Mp,
  init: Ip,
  insert: Pp,
  noop: Fp,
  safe_not_equal: Up,
  svg_element: zp
} = window.__gradio__svelte__internal, {
  SvelteComponent: Hp,
  append: Bp,
  attr: Gp,
  detach: Wp,
  init: Vp,
  insert: Yp,
  noop: jp,
  safe_not_equal: Xp,
  svg_element: Zp
} = window.__gradio__svelte__internal, {
  SvelteComponent: Kp,
  append: Jp,
  attr: Qp,
  detach: xp,
  init: e1,
  insert: t1,
  noop: n1,
  safe_not_equal: o1,
  svg_element: l1
} = window.__gradio__svelte__internal, {
  SvelteComponent: i1,
  append: a1,
  attr: s1,
  detach: r1,
  init: _1,
  insert: f1,
  noop: c1,
  safe_not_equal: u1,
  svg_element: d1,
  text: m1
} = window.__gradio__svelte__internal, {
  SvelteComponent: p1,
  append: g1,
  attr: h1,
  detach: b1,
  init: v1,
  insert: w1,
  noop: S1,
  safe_not_equal: T1,
  svg_element: C1,
  text: E1
} = window.__gradio__svelte__internal, {
  SvelteComponent: k1,
  append: A1,
  attr: y1,
  detach: $1,
  init: L1,
  insert: q1,
  noop: R1,
  safe_not_equal: O1,
  svg_element: N1,
  text: D1
} = window.__gradio__svelte__internal, {
  SvelteComponent: M1,
  append: I1,
  attr: P1,
  detach: F1,
  init: U1,
  insert: z1,
  noop: H1,
  safe_not_equal: B1,
  svg_element: G1
} = window.__gradio__svelte__internal, {
  SvelteComponent: W1,
  append: V1,
  attr: Y1,
  detach: j1,
  init: X1,
  insert: Z1,
  noop: K1,
  safe_not_equal: J1,
  svg_element: Q1
} = window.__gradio__svelte__internal, ra = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Qn = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
ra.reduce((n, { color: e, primary: t, secondary: o }) => ({
  ...n,
  [e]: {
    primary: Qn[e][t],
    secondary: Qn[e][o]
  }
}), {});
const {
  SvelteComponent: x1,
  create_component: eg,
  destroy_component: tg,
  init: ng,
  mount_component: og,
  safe_not_equal: lg,
  transition_in: ig,
  transition_out: ag
} = window.__gradio__svelte__internal, { createEventDispatcher: sg } = window.__gradio__svelte__internal, {
  SvelteComponent: rg,
  append: _g,
  attr: fg,
  check_outros: cg,
  create_component: ug,
  destroy_component: dg,
  detach: mg,
  element: pg,
  group_outros: gg,
  init: hg,
  insert: bg,
  mount_component: vg,
  safe_not_equal: wg,
  set_data: Sg,
  space: Tg,
  text: Cg,
  toggle_class: Eg,
  transition_in: kg,
  transition_out: Ag
} = window.__gradio__svelte__internal, {
  SvelteComponent: yg,
  attr: $g,
  create_slot: Lg,
  detach: qg,
  element: Rg,
  get_all_dirty_from_scope: Og,
  get_slot_changes: Ng,
  init: Dg,
  insert: Mg,
  safe_not_equal: Ig,
  toggle_class: Pg,
  transition_in: Fg,
  transition_out: Ug,
  update_slot_base: zg
} = window.__gradio__svelte__internal, {
  SvelteComponent: Hg,
  append: Bg,
  attr: Gg,
  check_outros: Wg,
  create_component: Vg,
  destroy_component: Yg,
  detach: jg,
  element: Xg,
  empty: Zg,
  group_outros: Kg,
  init: Jg,
  insert: Qg,
  listen: xg,
  mount_component: eh,
  safe_not_equal: th,
  space: nh,
  toggle_class: oh,
  transition_in: lh,
  transition_out: ih
} = window.__gradio__svelte__internal;
function Ht() {
}
function _a(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function xn(n) {
  const e = typeof n == "string" && n.match(/^\s*(-?[\d.]+)([^\s]*)\s*$/);
  return e ? [parseFloat(e[1]), e[2] || "px"] : [
    /** @type {number} */
    n,
    "px"
  ];
}
const Ko = typeof window < "u";
let eo = Ko ? () => window.performance.now() : () => Date.now(), Jo = Ko ? (n) => requestAnimationFrame(n) : Ht;
const _t = /* @__PURE__ */ new Set();
function Qo(n) {
  _t.forEach((e) => {
    e.c(n) || (_t.delete(e), e.f());
  }), _t.size !== 0 && Jo(Qo);
}
function fa(n) {
  let e;
  return _t.size === 0 && Jo(Qo), {
    promise: new Promise((t) => {
      _t.add(e = { c: n, f: t });
    }),
    abort() {
      _t.delete(e);
    }
  };
}
function ca(n) {
  const e = n - 1;
  return e * e * e + 1;
}
function to(n, { delay: e = 0, duration: t = 400, easing: o = ca, x: l = 0, y: i = 0, opacity: a = 0 } = {}) {
  const r = getComputedStyle(n), s = +r.opacity, _ = r.transform === "none" ? "" : r.transform, c = s * (1 - a), [d, h] = xn(l), [b, S] = xn(i);
  return {
    delay: e,
    duration: t,
    easing: o,
    css: (E, A) => `
			transform: ${_} translate(${(1 - E) * d}${h}, ${(1 - E) * b}${S});
			opacity: ${s - c * A}`
  };
}
const it = [];
function ua(n, e = Ht) {
  let t;
  const o = /* @__PURE__ */ new Set();
  function l(r) {
    if (_a(n, r) && (n = r, t)) {
      const s = !it.length;
      for (const _ of o)
        _[1](), it.push(_, n);
      if (s) {
        for (let _ = 0; _ < it.length; _ += 2)
          it[_][0](it[_ + 1]);
        it.length = 0;
      }
    }
  }
  function i(r) {
    l(r(n));
  }
  function a(r, s = Ht) {
    const _ = [r, s];
    return o.add(_), o.size === 1 && (t = e(l, i) || Ht), r(n), () => {
      o.delete(_), o.size === 0 && t && (t(), t = null);
    };
  }
  return { set: l, update: i, subscribe: a };
}
function no(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function pn(n, e, t, o) {
  if (typeof t == "number" || no(t)) {
    const l = o - t, i = (t - e) / (n.dt || 1 / 60), a = n.opts.stiffness * l, r = n.opts.damping * i, s = (a - r) * n.inv_mass, _ = (i + s) * n.dt;
    return Math.abs(_) < n.opts.precision && Math.abs(l) < n.opts.precision ? o : (n.settled = !1, no(t) ? new Date(t.getTime() + _) : t + _);
  } else {
    if (Array.isArray(t))
      return t.map(
        (l, i) => pn(n, e[i], t[i], o[i])
      );
    if (typeof t == "object") {
      const l = {};
      for (const i in t)
        l[i] = pn(n, e[i], t[i], o[i]);
      return l;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function oo(n, e = {}) {
  const t = ua(n), { stiffness: o = 0.15, damping: l = 0.8, precision: i = 0.01 } = e;
  let a, r, s, _ = n, c = n, d = 1, h = 0, b = !1;
  function S(A, q = {}) {
    c = A;
    const g = s = {};
    return n == null || q.hard || E.stiffness >= 1 && E.damping >= 1 ? (b = !0, a = eo(), _ = A, t.set(n = c), Promise.resolve()) : (q.soft && (h = 1 / ((q.soft === !0 ? 0.5 : +q.soft) * 60), d = 0), r || (a = eo(), b = !1, r = fa((m) => {
      if (b)
        return b = !1, r = null, !1;
      d = Math.min(d + h, 1);
      const p = {
        inv_mass: d,
        opts: E,
        settled: !0,
        dt: (m - a) * 60 / 1e3
      }, y = pn(p, _, n, c);
      return a = m, _ = n, t.set(n = y), p.settled && (r = null), !p.settled;
    })), new Promise((m) => {
      r.promise.then(() => {
        g === s && m();
      });
    }));
  }
  const E = {
    set: S,
    update: (A, q) => S(A(c, n), q),
    subscribe: t.subscribe,
    stiffness: o,
    damping: l,
    precision: i
  };
  return E;
}
const {
  SvelteComponent: da,
  add_render_callback: xo,
  append: Nt,
  attr: ne,
  binding_callbacks: lo,
  check_outros: ma,
  create_bidirectional_transition: io,
  destroy_each: pa,
  detach: Ct,
  element: Gt,
  empty: ga,
  ensure_array_like: ao,
  group_outros: ha,
  init: ba,
  insert: Et,
  listen: gn,
  prevent_default: va,
  run_all: wa,
  safe_not_equal: Sa,
  set_data: Ta,
  set_style: ke,
  space: hn,
  text: Ca,
  toggle_class: Ee,
  transition_in: an,
  transition_out: so
} = window.__gradio__svelte__internal, { createEventDispatcher: Ea } = window.__gradio__svelte__internal;
function ro(n, e, t) {
  const o = n.slice();
  return o[26] = e[t], o;
}
function _o(n) {
  let e, t, o, l, i, a = ao(
    /*filtered_indices*/
    n[1]
  ), r = [];
  for (let s = 0; s < a.length; s += 1)
    r[s] = fo(ro(n, a, s));
  return {
    c() {
      e = Gt("ul");
      for (let s = 0; s < r.length; s += 1)
        r[s].c();
      ne(e, "class", "options svelte-wmd465"), ne(e, "role", "listbox"), ke(
        e,
        "top",
        /*top*/
        n[9]
      ), ke(
        e,
        "bottom",
        /*bottom*/
        n[10]
      ), ke(e, "max-height", `calc(${/*max_height*/
      n[11]}px - var(--window-padding))`), ke(
        e,
        "width",
        /*input_width*/
        n[8] + "px"
      );
    },
    m(s, _) {
      Et(s, e, _);
      for (let c = 0; c < r.length; c += 1)
        r[c] && r[c].m(e, null);
      n[23](e), o = !0, l || (i = gn(e, "mousedown", va(
        /*mousedown_handler*/
        n[22]
      )), l = !0);
    },
    p(s, _) {
      if (_ & /*filtered_indices, choices, selected_indices, active_index, input_width*/
      307) {
        a = ao(
          /*filtered_indices*/
          s[1]
        );
        let c;
        for (c = 0; c < a.length; c += 1) {
          const d = ro(s, a, c);
          r[c] ? r[c].p(d, _) : (r[c] = fo(d), r[c].c(), r[c].m(e, null));
        }
        for (; c < r.length; c += 1)
          r[c].d(1);
        r.length = a.length;
      }
      _ & /*top*/
      512 && ke(
        e,
        "top",
        /*top*/
        s[9]
      ), _ & /*bottom*/
      1024 && ke(
        e,
        "bottom",
        /*bottom*/
        s[10]
      ), _ & /*max_height*/
      2048 && ke(e, "max-height", `calc(${/*max_height*/
      s[11]}px - var(--window-padding))`), _ & /*input_width*/
      256 && ke(
        e,
        "width",
        /*input_width*/
        s[8] + "px"
      );
    },
    i(s) {
      o || (s && xo(() => {
        o && (t || (t = io(e, to, { duration: 200, y: 5 }, !0)), t.run(1));
      }), o = !0);
    },
    o(s) {
      s && (t || (t = io(e, to, { duration: 200, y: 5 }, !1)), t.run(0)), o = !1;
    },
    d(s) {
      s && Ct(e), pa(r, s), n[23](null), s && t && t.end(), l = !1, i();
    }
  };
}
function fo(n) {
  let e, t, o, l = (
    /*choices*/
    n[0][
      /*index*/
      n[26]
    ][0] + ""
  ), i, a, r, s, _;
  return {
    c() {
      e = Gt("li"), t = Gt("span"), t.textContent = "✓", o = hn(), i = Ca(l), a = hn(), ne(t, "class", "inner-item svelte-wmd465"), Ee(t, "hide", !/*selected_indices*/
      n[4].includes(
        /*index*/
        n[26]
      )), ne(e, "class", "item svelte-wmd465"), ne(e, "data-index", r = /*index*/
      n[26]), ne(e, "aria-label", s = /*choices*/
      n[0][
        /*index*/
        n[26]
      ][0]), ne(e, "data-testid", "dropdown-option"), ne(e, "role", "option"), ne(e, "aria-selected", _ = /*selected_indices*/
      n[4].includes(
        /*index*/
        n[26]
      )), Ee(
        e,
        "selected",
        /*selected_indices*/
        n[4].includes(
          /*index*/
          n[26]
        )
      ), Ee(
        e,
        "active",
        /*index*/
        n[26] === /*active_index*/
        n[5]
      ), Ee(
        e,
        "bg-gray-100",
        /*index*/
        n[26] === /*active_index*/
        n[5]
      ), Ee(
        e,
        "dark:bg-gray-600",
        /*index*/
        n[26] === /*active_index*/
        n[5]
      ), ke(
        e,
        "width",
        /*input_width*/
        n[8] + "px"
      );
    },
    m(c, d) {
      Et(c, e, d), Nt(e, t), Nt(e, o), Nt(e, i), Nt(e, a);
    },
    p(c, d) {
      d & /*selected_indices, filtered_indices*/
      18 && Ee(t, "hide", !/*selected_indices*/
      c[4].includes(
        /*index*/
        c[26]
      )), d & /*choices, filtered_indices*/
      3 && l !== (l = /*choices*/
      c[0][
        /*index*/
        c[26]
      ][0] + "") && Ta(i, l), d & /*filtered_indices*/
      2 && r !== (r = /*index*/
      c[26]) && ne(e, "data-index", r), d & /*choices, filtered_indices*/
      3 && s !== (s = /*choices*/
      c[0][
        /*index*/
        c[26]
      ][0]) && ne(e, "aria-label", s), d & /*selected_indices, filtered_indices*/
      18 && _ !== (_ = /*selected_indices*/
      c[4].includes(
        /*index*/
        c[26]
      )) && ne(e, "aria-selected", _), d & /*selected_indices, filtered_indices*/
      18 && Ee(
        e,
        "selected",
        /*selected_indices*/
        c[4].includes(
          /*index*/
          c[26]
        )
      ), d & /*filtered_indices, active_index*/
      34 && Ee(
        e,
        "active",
        /*index*/
        c[26] === /*active_index*/
        c[5]
      ), d & /*filtered_indices, active_index*/
      34 && Ee(
        e,
        "bg-gray-100",
        /*index*/
        c[26] === /*active_index*/
        c[5]
      ), d & /*filtered_indices, active_index*/
      34 && Ee(
        e,
        "dark:bg-gray-600",
        /*index*/
        c[26] === /*active_index*/
        c[5]
      ), d & /*input_width*/
      256 && ke(
        e,
        "width",
        /*input_width*/
        c[8] + "px"
      );
    },
    d(c) {
      c && Ct(e);
    }
  };
}
function ka(n) {
  let e, t, o, l, i;
  xo(
    /*onwindowresize*/
    n[20]
  );
  let a = (
    /*show_options*/
    n[2] && !/*disabled*/
    n[3] && _o(n)
  );
  return {
    c() {
      e = Gt("div"), t = hn(), a && a.c(), o = ga(), ne(e, "class", "reference");
    },
    m(r, s) {
      Et(r, e, s), n[21](e), Et(r, t, s), a && a.m(r, s), Et(r, o, s), l || (i = [
        gn(
          window,
          "scroll",
          /*scroll_listener*/
          n[13]
        ),
        gn(
          window,
          "resize",
          /*onwindowresize*/
          n[20]
        )
      ], l = !0);
    },
    p(r, [s]) {
      /*show_options*/
      r[2] && !/*disabled*/
      r[3] ? a ? (a.p(r, s), s & /*show_options, disabled*/
      12 && an(a, 1)) : (a = _o(r), a.c(), an(a, 1), a.m(o.parentNode, o)) : a && (ha(), so(a, 1, 1, () => {
        a = null;
      }), ma());
    },
    i(r) {
      an(a);
    },
    o(r) {
      so(a);
    },
    d(r) {
      r && (Ct(e), Ct(t), Ct(o)), n[21](null), a && a.d(r), l = !1, wa(i);
    }
  };
}
function Aa(n, e, t) {
  var o, l;
  let { choices: i } = e, { filtered_indices: a } = e, { show_options: r = !1 } = e, { disabled: s = !1 } = e, { selected_indices: _ = [] } = e, { active_index: c = null } = e, d, h, b, S, E, A, q, g, m, p;
  function y() {
    const { top: R, bottom: T } = E.getBoundingClientRect();
    t(17, d = R), t(18, h = p - T);
  }
  let w = null;
  function N() {
    r && (w !== null && clearTimeout(w), w = setTimeout(
      () => {
        y(), w = null;
      },
      10
    ));
  }
  const P = Ea();
  function I() {
    t(12, p = window.innerHeight);
  }
  function W(R) {
    lo[R ? "unshift" : "push"](() => {
      E = R, t(6, E);
    });
  }
  const D = (R) => P("change", R);
  function Y(R) {
    lo[R ? "unshift" : "push"](() => {
      A = R, t(7, A);
    });
  }
  return n.$$set = (R) => {
    "choices" in R && t(0, i = R.choices), "filtered_indices" in R && t(1, a = R.filtered_indices), "show_options" in R && t(2, r = R.show_options), "disabled" in R && t(3, s = R.disabled), "selected_indices" in R && t(4, _ = R.selected_indices), "active_index" in R && t(5, c = R.active_index);
  }, n.$$.update = () => {
    if (n.$$.dirty & /*show_options, refElement, listElement, selected_indices, _a, _b, distance_from_bottom, distance_from_top, input_height*/
    1016020) {
      if (r && E) {
        if (A && _.length > 0) {
          let T = A.querySelectorAll("li");
          for (const ie of Array.from(T))
            if (ie.getAttribute("data-index") === _[0].toString()) {
              t(15, o = A == null ? void 0 : A.scrollTo) === null || o === void 0 || o.call(A, 0, ie.offsetTop);
              break;
            }
        }
        y();
        const R = t(16, l = E.parentElement) === null || l === void 0 ? void 0 : l.getBoundingClientRect();
        t(19, b = (R == null ? void 0 : R.height) || 0), t(8, S = (R == null ? void 0 : R.width) || 0);
      }
      h > d ? (t(9, q = `${d}px`), t(11, m = h), t(10, g = null)) : (t(10, g = `${h + b}px`), t(11, m = d - b), t(9, q = null));
    }
  }, [
    i,
    a,
    r,
    s,
    _,
    c,
    E,
    A,
    S,
    q,
    g,
    m,
    p,
    N,
    P,
    o,
    l,
    d,
    h,
    b,
    I,
    W,
    D,
    Y
  ];
}
class ya extends da {
  constructor(e) {
    super(), ba(this, e, Aa, ka, Sa, {
      choices: 0,
      filtered_indices: 1,
      show_options: 2,
      disabled: 3,
      selected_indices: 4,
      active_index: 5
    });
  }
}
function $a(n, e) {
  return (n % e + e) % e;
}
function La(n, e) {
  return n.reduce((t, o, l) => ((!e || o[0].toLowerCase().includes(e.toLowerCase())) && t.push(l), t), []);
}
function qa(n, e, t) {
  n("change", e), t || n("input");
}
function Ra(n, e, t) {
  if (n.key === "Escape")
    return [!1, e];
  if ((n.key === "ArrowDown" || n.key === "ArrowUp") && t.length >= 0)
    if (e === null)
      e = n.key === "ArrowDown" ? t[0] : t[t.length - 1];
    else {
      const o = t.indexOf(e), l = n.key === "ArrowUp" ? -1 : 1;
      e = t[$a(o + l, t.length)];
    }
  return [!0, e];
}
const {
  SvelteComponent: Oa,
  append: De,
  attr: re,
  binding_callbacks: Na,
  check_outros: el,
  create_component: Wt,
  destroy_component: Vt,
  detach: oe,
  element: We,
  group_outros: tl,
  init: Da,
  insert: le,
  listen: Ve,
  mount_component: Yt,
  noop: Ma,
  run_all: nl,
  safe_not_equal: Ia,
  set_data: ft,
  set_input_value: co,
  space: st,
  text: Pe,
  toggle_class: at,
  transition_in: Ae,
  transition_out: Me
} = window.__gradio__svelte__internal, { afterUpdate: Pa, createEventDispatcher: Fa } = window.__gradio__svelte__internal;
function Ua(n) {
  let e;
  return {
    c() {
      e = Pe(
        /*label*/
        n[0]
      );
    },
    m(t, o) {
      le(t, e, o);
    },
    p(t, o) {
      o[0] & /*label*/
      1 && ft(
        e,
        /*label*/
        t[0]
      );
    },
    d(t) {
      t && oe(e);
    }
  };
}
function za(n) {
  let e = (
    /*selected_indices*/
    n[12].length + ""
  ), t, o, l = (
    /*selected_indices*/
    n[12].length % 10 === 1 && /*selected_indices*/
    n[12].length % 100 !== 11 ? "источник" : (
      /*selected_indices*/
      n[12].length % 10 >= 2 && /*selected_indices*/
      n[12].length % 10 <= 4 && /*selected_indices*/
      (n[12].length % 100 < 10 || /*selected_indices*/
      n[12].length % 100 >= 20) ? "источника" : "источников"
    )
  ), i;
  return {
    c() {
      t = Pe(e), o = st(), i = Pe(l);
    },
    m(a, r) {
      le(a, t, r), le(a, o, r), le(a, i, r);
    },
    p(a, r) {
      r[0] & /*selected_indices*/
      4096 && e !== (e = /*selected_indices*/
      a[12].length + "") && ft(t, e), r[0] & /*selected_indices*/
      4096 && l !== (l = /*selected_indices*/
      a[12].length % 10 === 1 && /*selected_indices*/
      a[12].length % 100 !== 11 ? "источник" : (
        /*selected_indices*/
        a[12].length % 10 >= 2 && /*selected_indices*/
        a[12].length % 10 <= 4 && /*selected_indices*/
        (a[12].length % 100 < 10 || /*selected_indices*/
        a[12].length % 100 >= 20) ? "источника" : "источников"
      )) && ft(i, l);
    },
    d(a) {
      a && (oe(t), oe(o), oe(i));
    }
  };
}
function Ha(n) {
  let e = (
    /*choices_names*/
    n[15][
      /*selected_indices*/
      n[12][0]
    ] + ""
  ), t, o, l = (
    /*choices_names*/
    n[15][
      /*selected_indices*/
      n[12][1]
    ] + ""
  ), i;
  return {
    c() {
      t = Pe(e), o = Pe(", "), i = Pe(l);
    },
    m(a, r) {
      le(a, t, r), le(a, o, r), le(a, i, r);
    },
    p(a, r) {
      r[0] & /*choices_names, selected_indices*/
      36864 && e !== (e = /*choices_names*/
      a[15][
        /*selected_indices*/
        a[12][0]
      ] + "") && ft(t, e), r[0] & /*choices_names, selected_indices*/
      36864 && l !== (l = /*choices_names*/
      a[15][
        /*selected_indices*/
        a[12][1]
      ] + "") && ft(i, l);
    },
    d(a) {
      a && (oe(t), oe(o), oe(i));
    }
  };
}
function Ba(n) {
  let e = (
    /*choices_names*/
    n[15][
      /*selected_indices*/
      n[12][0]
    ] + ""
  ), t;
  return {
    c() {
      t = Pe(e);
    },
    m(o, l) {
      le(o, t, l);
    },
    p(o, l) {
      l[0] & /*choices_names, selected_indices*/
      36864 && e !== (e = /*choices_names*/
      o[15][
        /*selected_indices*/
        o[12][0]
      ] + "") && ft(t, e);
    },
    d(o) {
      o && oe(t);
    }
  };
}
function Ga(n) {
  let e;
  return {
    c() {
      e = Pe("Все источники");
    },
    m(t, o) {
      le(t, e, o);
    },
    p: Ma,
    d(t) {
      t && oe(e);
    }
  };
}
function uo(n) {
  let e, t, o, l, i = (
    /*selected_indices*/
    n[12].length > 0 && mo(n)
  );
  return o = new xi({}), {
    c() {
      i && i.c(), e = st(), t = We("span"), Wt(o.$$.fragment), re(t, "class", "icon-wrap svelte-19ik8fr");
    },
    m(a, r) {
      i && i.m(a, r), le(a, e, r), le(a, t, r), Yt(o, t, null), l = !0;
    },
    p(a, r) {
      /*selected_indices*/
      a[12].length > 0 ? i ? (i.p(a, r), r[0] & /*selected_indices*/
      4096 && Ae(i, 1)) : (i = mo(a), i.c(), Ae(i, 1), i.m(e.parentNode, e)) : i && (tl(), Me(i, 1, 1, () => {
        i = null;
      }), el());
    },
    i(a) {
      l || (Ae(i), Ae(o.$$.fragment, a), l = !0);
    },
    o(a) {
      Me(i), Me(o.$$.fragment, a), l = !1;
    },
    d(a) {
      a && (oe(e), oe(t)), i && i.d(a), Vt(o);
    }
  };
}
function mo(n) {
  let e, t, o, l, i, a;
  return t = new sa({}), {
    c() {
      e = We("div"), Wt(t.$$.fragment), re(e, "role", "button"), re(e, "tabindex", "0"), re(e, "class", "token-remove remove-all svelte-19ik8fr"), re(e, "title", o = /*i18n*/
      n[9]("common.clear"));
    },
    m(r, s) {
      le(r, e, s), Yt(t, e, null), l = !0, i || (a = [
        Ve(
          e,
          "click",
          /*remove_all*/
          n[20]
        ),
        Ve(
          e,
          "keydown",
          /*keydown_handler*/
          n[33]
        )
      ], i = !0);
    },
    p(r, s) {
      (!l || s[0] & /*i18n*/
      512 && o !== (o = /*i18n*/
      r[9]("common.clear"))) && re(e, "title", o);
    },
    i(r) {
      l || (Ae(t.$$.fragment, r), l = !0);
    },
    o(r) {
      Me(t.$$.fragment, r), l = !1;
    },
    d(r) {
      r && oe(e), Vt(t), i = !1, nl(a);
    }
  };
}
function Wa(n) {
  let e, t, o, l, i, a, r, s, _, c, d, h, b, S, E;
  t = new Ti({
    props: {
      show_label: (
        /*show_label*/
        n[5]
      ),
      info: (
        /*info*/
        n[1]
      ),
      $$slots: { default: [Ua] },
      $$scope: { ctx: n }
    }
  });
  function A(p, y) {
    if (
      /*selected_indices*/
      p[12].length === /*choices_names*/
      p[15].length
    ) return Ga;
    if (
      /*selected_indices*/
      p[12].length === 1
    ) return Ba;
    if (
      /*selected_indices*/
      p[12].length === 2
    ) return Ha;
    if (
      /*selected_indices*/
      p[12].length > 2
    ) return za;
  }
  let q = A(n), g = q && q(n), m = !/*disabled*/
  n[4] && uo(n);
  return h = new ya({
    props: {
      show_options: (
        /*show_options*/
        n[14]
      ),
      choices: (
        /*choices*/
        n[3]
      ),
      filtered_indices: (
        /*filtered_indices*/
        n[11]
      ),
      disabled: (
        /*disabled*/
        n[4]
      ),
      selected_indices: (
        /*selected_indices*/
        n[12]
      ),
      active_index: (
        /*active_index*/
        n[16]
      )
    }
  }), h.$on(
    "change",
    /*handle_option_selected*/
    n[19]
  ), {
    c() {
      e = We("label"), Wt(t.$$.fragment), o = st(), l = We("div"), i = We("div"), g && g.c(), a = st(), r = We("div"), s = We("input"), c = st(), m && m.c(), d = st(), Wt(h.$$.fragment), re(s, "class", "border-none svelte-19ik8fr"), s.disabled = /*disabled*/
      n[4], re(s, "autocomplete", "off"), s.readOnly = _ = !/*filterable*/
      n[8], at(s, "subdued", !/*choices_names*/
      n[15].includes(
        /*input_text*/
        n[10]
      ) && !/*allow_custom_value*/
      n[7] || /*selected_indices*/
      n[12].length === /*max_choices*/
      n[2]), re(r, "class", "secondary-wrap svelte-19ik8fr"), re(i, "class", "wrap-inner svelte-19ik8fr"), at(
        i,
        "show_options",
        /*show_options*/
        n[14]
      ), re(l, "class", "wrap svelte-19ik8fr"), re(e, "class", "svelte-19ik8fr"), at(
        e,
        "container",
        /*container*/
        n[6]
      );
    },
    m(p, y) {
      le(p, e, y), Yt(t, e, null), De(e, o), De(e, l), De(l, i), g && g.m(i, null), De(i, a), De(i, r), De(r, s), co(
        s,
        /*input_text*/
        n[10]
      ), n[31](s), De(r, c), m && m.m(r, null), De(l, d), Yt(h, l, null), b = !0, S || (E = [
        Ve(
          s,
          "input",
          /*input_input_handler*/
          n[30]
        ),
        Ve(
          s,
          "keydown",
          /*handle_key_down*/
          n[22]
        ),
        Ve(
          s,
          "keyup",
          /*keyup_handler*/
          n[32]
        ),
        Ve(
          s,
          "blur",
          /*handle_blur*/
          n[18]
        ),
        Ve(
          s,
          "focus",
          /*handle_focus*/
          n[21]
        )
      ], S = !0);
    },
    p(p, y) {
      const w = {};
      y[0] & /*show_label*/
      32 && (w.show_label = /*show_label*/
      p[5]), y[0] & /*info*/
      2 && (w.info = /*info*/
      p[1]), y[0] & /*label*/
      1 | y[1] & /*$$scope*/
      128 && (w.$$scope = { dirty: y, ctx: p }), t.$set(w), q === (q = A(p)) && g ? g.p(p, y) : (g && g.d(1), g = q && q(p), g && (g.c(), g.m(i, a))), (!b || y[0] & /*disabled*/
      16) && (s.disabled = /*disabled*/
      p[4]), (!b || y[0] & /*filterable*/
      256 && _ !== (_ = !/*filterable*/
      p[8])) && (s.readOnly = _), y[0] & /*input_text*/
      1024 && s.value !== /*input_text*/
      p[10] && co(
        s,
        /*input_text*/
        p[10]
      ), (!b || y[0] & /*choices_names, input_text, allow_custom_value, selected_indices, max_choices*/
      38020) && at(s, "subdued", !/*choices_names*/
      p[15].includes(
        /*input_text*/
        p[10]
      ) && !/*allow_custom_value*/
      p[7] || /*selected_indices*/
      p[12].length === /*max_choices*/
      p[2]), /*disabled*/
      p[4] ? m && (tl(), Me(m, 1, 1, () => {
        m = null;
      }), el()) : m ? (m.p(p, y), y[0] & /*disabled*/
      16 && Ae(m, 1)) : (m = uo(p), m.c(), Ae(m, 1), m.m(r, null)), (!b || y[0] & /*show_options*/
      16384) && at(
        i,
        "show_options",
        /*show_options*/
        p[14]
      );
      const N = {};
      y[0] & /*show_options*/
      16384 && (N.show_options = /*show_options*/
      p[14]), y[0] & /*choices*/
      8 && (N.choices = /*choices*/
      p[3]), y[0] & /*filtered_indices*/
      2048 && (N.filtered_indices = /*filtered_indices*/
      p[11]), y[0] & /*disabled*/
      16 && (N.disabled = /*disabled*/
      p[4]), y[0] & /*selected_indices*/
      4096 && (N.selected_indices = /*selected_indices*/
      p[12]), y[0] & /*active_index*/
      65536 && (N.active_index = /*active_index*/
      p[16]), h.$set(N), (!b || y[0] & /*container*/
      64) && at(
        e,
        "container",
        /*container*/
        p[6]
      );
    },
    i(p) {
      b || (Ae(t.$$.fragment, p), Ae(m), Ae(h.$$.fragment, p), b = !0);
    },
    o(p) {
      Me(t.$$.fragment, p), Me(m), Me(h.$$.fragment, p), b = !1;
    },
    d(p) {
      p && oe(e), Vt(t), g && g.d(), n[31](null), m && m.d(), Vt(h), S = !1, nl(E);
    }
  };
}
function Va(n, e, t) {
  let { label: o } = e, { info: l = void 0 } = e, { value: i = [] } = e, a = [], { value_is_output: r = !1 } = e, { max_choices: s = null } = e, { choices: _ } = e, c, { disabled: d = !1 } = e, { show_label: h } = e, { container: b = !0 } = e, { allow_custom_value: S = !1 } = e, { filterable: E = !0 } = e, { i18n: A } = e, q, g = "", m = "", p = !1, y, w, N = [], P = null, I = [], W = [];
  const D = Fa();
  Array.isArray(i) && i.forEach((u) => {
    const B = _.map((ae) => ae[1]).indexOf(u);
    B !== -1 ? I.push(B) : I.push(u);
  });
  function Y() {
    S || t(10, g = ""), S && g !== "" && (T(g), t(10, g = "")), t(14, p = !1), t(16, P = null), D("blur");
  }
  function R(u) {
    t(12, I = I.filter((B) => B !== u)), D("select", {
      index: typeof u == "number" ? u : -1,
      value: typeof u == "number" ? w[u] : u,
      selected: !1
    });
  }
  function T(u) {
    (s === null || I.length < s) && (t(12, I = [...I, u]), D("select", {
      index: typeof u == "number" ? u : -1,
      value: typeof u == "number" ? w[u] : u,
      selected: !0
    })), I.length === s && (t(14, p = !1), t(16, P = null), q.blur());
  }
  function ie(u) {
    const B = parseInt(u.detail.target.dataset.index);
    ee(B);
  }
  function ee(u) {
    I.includes(u) ? R(u) : T(u), t(10, g = "");
  }
  function Fe(u) {
    t(12, I = []), t(10, g = ""), u.preventDefault();
  }
  function je(u) {
    t(11, N = _.map((B, ae) => ae)), (s === null || I.length < s) && t(14, p = !0), D("focus");
  }
  function Xe(u) {
    t(14, [p, P] = Ra(u, P, N), p, (t(16, P), t(3, _), t(26, c), t(10, g), t(27, m), t(7, S), t(11, N))), u.key === "Enter" && (P !== null ? ee(P) : S && (T(g), t(10, g = ""))), u.key === "Backspace" && g === "" && t(12, I = [...I.slice(0, -1)]), I.length === s && (t(14, p = !1), t(16, P = null));
  }
  function Ue() {
    i === void 0 ? t(12, I = []) : Array.isArray(i) && t(12, I = i.map((u) => {
      const B = w.indexOf(u);
      if (B !== -1)
        return B;
      if (S)
        return u;
    }).filter((u) => u !== void 0));
  }
  Pa(() => {
    t(24, r = !1);
  });
  function F() {
    g = this.value, t(10, g);
  }
  function Ze(u) {
    Na[u ? "unshift" : "push"](() => {
      q = u, t(13, q);
    });
  }
  const H = (u) => D("key_up", { key: u.key, input_value: g }), Ke = (u) => {
    u.key === "Enter" && Fe(u);
  };
  return n.$$set = (u) => {
    "label" in u && t(0, o = u.label), "info" in u && t(1, l = u.info), "value" in u && t(23, i = u.value), "value_is_output" in u && t(24, r = u.value_is_output), "max_choices" in u && t(2, s = u.max_choices), "choices" in u && t(3, _ = u.choices), "disabled" in u && t(4, d = u.disabled), "show_label" in u && t(5, h = u.show_label), "container" in u && t(6, b = u.container), "allow_custom_value" in u && t(7, S = u.allow_custom_value), "filterable" in u && t(8, E = u.filterable), "i18n" in u && t(9, A = u.i18n);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*choices*/
    8 && (t(15, y = _.map((u) => u[0])), t(28, w = _.map((u) => u[1]))), n.$$.dirty[0] & /*choices, old_choices, input_text, old_input_text, allow_custom_value, filtered_indices*/
    201329800 && (_ !== c || g !== m) && (t(11, N = La(_, g)), t(26, c = _), t(27, m = g), S || t(16, P = N[0])), n.$$.dirty[0] & /*selected_indices, old_selected_index, choices_values*/
    805310464 && JSON.stringify(I) != JSON.stringify(W) && (t(23, i = I.map((u) => typeof u == "number" ? w[u] : u)), t(29, W = I.slice())), n.$$.dirty[0] & /*value, old_value, value_is_output*/
    58720256 && JSON.stringify(i) != JSON.stringify(a) && (qa(D, i, r), t(25, a = Array.isArray(i) ? i.slice() : i)), n.$$.dirty[0] & /*value*/
    8388608 && Ue();
  }, [
    o,
    l,
    s,
    _,
    d,
    h,
    b,
    S,
    E,
    A,
    g,
    N,
    I,
    q,
    p,
    y,
    P,
    D,
    Y,
    ie,
    Fe,
    je,
    Xe,
    i,
    r,
    a,
    c,
    m,
    w,
    W,
    F,
    Ze,
    H,
    Ke
  ];
}
class Ya extends Oa {
  constructor(e) {
    super(), Da(
      this,
      e,
      Va,
      Wa,
      Ia,
      {
        label: 0,
        info: 1,
        value: 23,
        value_is_output: 24,
        max_choices: 2,
        choices: 3,
        disabled: 4,
        show_label: 5,
        container: 6,
        allow_custom_value: 7,
        filterable: 8,
        i18n: 9
      },
      null,
      [-1, -1]
    );
  }
}
function rt(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let o = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + o;
}
const {
  SvelteComponent: ja,
  append: pe,
  attr: M,
  component_subscribe: po,
  detach: Xa,
  element: Za,
  init: Ka,
  insert: Ja,
  noop: go,
  safe_not_equal: Qa,
  set_style: Dt,
  svg_element: ge,
  toggle_class: ho
} = window.__gradio__svelte__internal, { onMount: xa } = window.__gradio__svelte__internal;
function es(n) {
  let e, t, o, l, i, a, r, s, _, c, d, h;
  return {
    c() {
      e = Za("div"), t = ge("svg"), o = ge("g"), l = ge("path"), i = ge("path"), a = ge("path"), r = ge("path"), s = ge("g"), _ = ge("path"), c = ge("path"), d = ge("path"), h = ge("path"), M(l, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), M(l, "fill", "#FF7C00"), M(l, "fill-opacity", "0.4"), M(l, "class", "svelte-43sxxs"), M(i, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), M(i, "fill", "#FF7C00"), M(i, "class", "svelte-43sxxs"), M(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), M(a, "fill", "#FF7C00"), M(a, "fill-opacity", "0.4"), M(a, "class", "svelte-43sxxs"), M(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), M(r, "fill", "#FF7C00"), M(r, "class", "svelte-43sxxs"), Dt(o, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), M(_, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), M(_, "fill", "#FF7C00"), M(_, "fill-opacity", "0.4"), M(_, "class", "svelte-43sxxs"), M(c, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), M(c, "fill", "#FF7C00"), M(c, "class", "svelte-43sxxs"), M(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), M(d, "fill", "#FF7C00"), M(d, "fill-opacity", "0.4"), M(d, "class", "svelte-43sxxs"), M(h, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), M(h, "fill", "#FF7C00"), M(h, "class", "svelte-43sxxs"), Dt(s, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), M(t, "viewBox", "-1200 -1200 3000 3000"), M(t, "fill", "none"), M(t, "xmlns", "http://www.w3.org/2000/svg"), M(t, "class", "svelte-43sxxs"), M(e, "class", "svelte-43sxxs"), ho(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(b, S) {
      Ja(b, e, S), pe(e, t), pe(t, o), pe(o, l), pe(o, i), pe(o, a), pe(o, r), pe(t, s), pe(s, _), pe(s, c), pe(s, d), pe(s, h);
    },
    p(b, [S]) {
      S & /*$top*/
      2 && Dt(o, "transform", "translate(" + /*$top*/
      b[1][0] + "px, " + /*$top*/
      b[1][1] + "px)"), S & /*$bottom*/
      4 && Dt(s, "transform", "translate(" + /*$bottom*/
      b[2][0] + "px, " + /*$bottom*/
      b[2][1] + "px)"), S & /*margin*/
      1 && ho(
        e,
        "margin",
        /*margin*/
        b[0]
      );
    },
    i: go,
    o: go,
    d(b) {
      b && Xa(e);
    }
  };
}
function ts(n, e, t) {
  let o, l;
  var i = this && this.__awaiter || function(b, S, E, A) {
    function q(g) {
      return g instanceof E ? g : new E(function(m) {
        m(g);
      });
    }
    return new (E || (E = Promise))(function(g, m) {
      function p(N) {
        try {
          w(A.next(N));
        } catch (P) {
          m(P);
        }
      }
      function y(N) {
        try {
          w(A.throw(N));
        } catch (P) {
          m(P);
        }
      }
      function w(N) {
        N.done ? g(N.value) : q(N.value).then(p, y);
      }
      w((A = A.apply(b, S || [])).next());
    });
  };
  let { margin: a = !0 } = e;
  const r = oo([0, 0]);
  po(n, r, (b) => t(1, o = b));
  const s = oo([0, 0]);
  po(n, s, (b) => t(2, l = b));
  let _;
  function c() {
    return i(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), s.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), s.set([125, -140])]), yield Promise.all([r.set([-125, 0]), s.set([125, -0])]), yield Promise.all([r.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function d() {
    return i(this, void 0, void 0, function* () {
      yield c(), _ || d();
    });
  }
  function h() {
    return i(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), s.set([-125, 0])]), d();
    });
  }
  return xa(() => (h(), () => _ = !0)), n.$$set = (b) => {
    "margin" in b && t(0, a = b.margin);
  }, [a, o, l, r, s];
}
class ns extends ja {
  constructor(e) {
    super(), Ka(this, e, ts, es, Qa, { margin: 0 });
  }
}
const {
  SvelteComponent: os,
  append: Ye,
  attr: ve,
  binding_callbacks: bo,
  check_outros: bn,
  create_component: ol,
  create_slot: ll,
  destroy_component: il,
  destroy_each: al,
  detach: $,
  element: ye,
  empty: ct,
  ensure_array_like: jt,
  get_all_dirty_from_scope: sl,
  get_slot_changes: rl,
  group_outros: vn,
  init: ls,
  insert: L,
  mount_component: _l,
  noop: wn,
  safe_not_equal: is,
  set_data: fe,
  set_style: Ie,
  space: _e,
  text: z,
  toggle_class: se,
  transition_in: be,
  transition_out: $e,
  update_slot_base: fl
} = window.__gradio__svelte__internal, { tick: as } = window.__gradio__svelte__internal, { onDestroy: ss } = window.__gradio__svelte__internal, { createEventDispatcher: rs } = window.__gradio__svelte__internal, _s = (n) => ({}), vo = (n) => ({}), fs = (n) => ({}), wo = (n) => ({});
function So(n, e, t) {
  const o = n.slice();
  return o[41] = e[t], o[43] = t, o;
}
function To(n, e, t) {
  const o = n.slice();
  return o[41] = e[t], o;
}
function cs(n) {
  let e, t, o, l, i = (
    /*i18n*/
    n[1]("common.error") + ""
  ), a, r, s;
  t = new Fi({
    props: {
      Icon: Vi,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const _ = (
    /*#slots*/
    n[30].error
  ), c = ll(
    _,
    n,
    /*$$scope*/
    n[29],
    vo
  );
  return {
    c() {
      e = ye("div"), ol(t.$$.fragment), o = _e(), l = ye("span"), a = z(i), r = _e(), c && c.c(), ve(e, "class", "clear-status svelte-v0wucf"), ve(l, "class", "error svelte-v0wucf");
    },
    m(d, h) {
      L(d, e, h), _l(t, e, null), L(d, o, h), L(d, l, h), Ye(l, a), L(d, r, h), c && c.m(d, h), s = !0;
    },
    p(d, h) {
      const b = {};
      h[0] & /*i18n*/
      2 && (b.label = /*i18n*/
      d[1]("common.clear")), t.$set(b), (!s || h[0] & /*i18n*/
      2) && i !== (i = /*i18n*/
      d[1]("common.error") + "") && fe(a, i), c && c.p && (!s || h[0] & /*$$scope*/
      536870912) && fl(
        c,
        _,
        d,
        /*$$scope*/
        d[29],
        s ? rl(
          _,
          /*$$scope*/
          d[29],
          h,
          _s
        ) : sl(
          /*$$scope*/
          d[29]
        ),
        vo
      );
    },
    i(d) {
      s || (be(t.$$.fragment, d), be(c, d), s = !0);
    },
    o(d) {
      $e(t.$$.fragment, d), $e(c, d), s = !1;
    },
    d(d) {
      d && ($(e), $(o), $(l), $(r)), il(t), c && c.d(d);
    }
  };
}
function us(n) {
  let e, t, o, l, i, a, r, s, _, c = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Co(n)
  );
  function d(m, p) {
    if (
      /*progress*/
      m[7]
    ) return ps;
    if (
      /*queue_position*/
      m[2] !== null && /*queue_size*/
      m[3] !== void 0 && /*queue_position*/
      m[2] >= 0
    ) return ms;
    if (
      /*queue_position*/
      m[2] === 0
    ) return ds;
  }
  let h = d(n), b = h && h(n), S = (
    /*timer*/
    n[5] && Ao(n)
  );
  const E = [vs, bs], A = [];
  function q(m, p) {
    return (
      /*last_progress_level*/
      m[15] != null ? 0 : (
        /*show_progress*/
        m[6] === "full" ? 1 : -1
      )
    );
  }
  ~(i = q(n)) && (a = A[i] = E[i](n));
  let g = !/*timer*/
  n[5] && No(n);
  return {
    c() {
      c && c.c(), e = _e(), t = ye("div"), b && b.c(), o = _e(), S && S.c(), l = _e(), a && a.c(), r = _e(), g && g.c(), s = ct(), ve(t, "class", "progress-text svelte-v0wucf"), se(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), se(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(m, p) {
      c && c.m(m, p), L(m, e, p), L(m, t, p), b && b.m(t, null), Ye(t, o), S && S.m(t, null), L(m, l, p), ~i && A[i].m(m, p), L(m, r, p), g && g.m(m, p), L(m, s, p), _ = !0;
    },
    p(m, p) {
      /*variant*/
      m[8] === "default" && /*show_eta_bar*/
      m[18] && /*show_progress*/
      m[6] === "full" ? c ? c.p(m, p) : (c = Co(m), c.c(), c.m(e.parentNode, e)) : c && (c.d(1), c = null), h === (h = d(m)) && b ? b.p(m, p) : (b && b.d(1), b = h && h(m), b && (b.c(), b.m(t, o))), /*timer*/
      m[5] ? S ? S.p(m, p) : (S = Ao(m), S.c(), S.m(t, null)) : S && (S.d(1), S = null), (!_ || p[0] & /*variant*/
      256) && se(
        t,
        "meta-text-center",
        /*variant*/
        m[8] === "center"
      ), (!_ || p[0] & /*variant*/
      256) && se(
        t,
        "meta-text",
        /*variant*/
        m[8] === "default"
      );
      let y = i;
      i = q(m), i === y ? ~i && A[i].p(m, p) : (a && (vn(), $e(A[y], 1, 1, () => {
        A[y] = null;
      }), bn()), ~i ? (a = A[i], a ? a.p(m, p) : (a = A[i] = E[i](m), a.c()), be(a, 1), a.m(r.parentNode, r)) : a = null), /*timer*/
      m[5] ? g && (vn(), $e(g, 1, 1, () => {
        g = null;
      }), bn()) : g ? (g.p(m, p), p[0] & /*timer*/
      32 && be(g, 1)) : (g = No(m), g.c(), be(g, 1), g.m(s.parentNode, s));
    },
    i(m) {
      _ || (be(a), be(g), _ = !0);
    },
    o(m) {
      $e(a), $e(g), _ = !1;
    },
    d(m) {
      m && ($(e), $(t), $(l), $(r), $(s)), c && c.d(m), b && b.d(), S && S.d(), ~i && A[i].d(m), g && g.d(m);
    }
  };
}
function Co(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = ye("div"), ve(e, "class", "eta-bar svelte-v0wucf"), Ie(e, "transform", t);
    },
    m(o, l) {
      L(o, e, l);
    },
    p(o, l) {
      l[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (o[17] || 0) * 100 - 100}%)`) && Ie(e, "transform", t);
    },
    d(o) {
      o && $(e);
    }
  };
}
function ds(n) {
  let e;
  return {
    c() {
      e = z("processing |");
    },
    m(t, o) {
      L(t, e, o);
    },
    p: wn,
    d(t) {
      t && $(e);
    }
  };
}
function ms(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), o, l, i, a;
  return {
    c() {
      e = z("queue: "), o = z(t), l = z("/"), i = z(
        /*queue_size*/
        n[3]
      ), a = z(" |");
    },
    m(r, s) {
      L(r, e, s), L(r, o, s), L(r, l, s), L(r, i, s), L(r, a, s);
    },
    p(r, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && fe(o, t), s[0] & /*queue_size*/
      8 && fe(
        i,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && ($(e), $(o), $(l), $(i), $(a));
    }
  };
}
function ps(n) {
  let e, t = jt(
    /*progress*/
    n[7]
  ), o = [];
  for (let l = 0; l < t.length; l += 1)
    o[l] = ko(To(n, t, l));
  return {
    c() {
      for (let l = 0; l < o.length; l += 1)
        o[l].c();
      e = ct();
    },
    m(l, i) {
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(l, i);
      L(l, e, i);
    },
    p(l, i) {
      if (i[0] & /*progress*/
      128) {
        t = jt(
          /*progress*/
          l[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = To(l, t, a);
          o[a] ? o[a].p(r, i) : (o[a] = ko(r), o[a].c(), o[a].m(e.parentNode, e));
        }
        for (; a < o.length; a += 1)
          o[a].d(1);
        o.length = t.length;
      }
    },
    d(l) {
      l && $(e), al(o, l);
    }
  };
}
function Eo(n) {
  let e, t = (
    /*p*/
    n[41].unit + ""
  ), o, l, i = " ", a;
  function r(c, d) {
    return (
      /*p*/
      c[41].length != null ? hs : gs
    );
  }
  let s = r(n), _ = s(n);
  return {
    c() {
      _.c(), e = _e(), o = z(t), l = z(" | "), a = z(i);
    },
    m(c, d) {
      _.m(c, d), L(c, e, d), L(c, o, d), L(c, l, d), L(c, a, d);
    },
    p(c, d) {
      s === (s = r(c)) && _ ? _.p(c, d) : (_.d(1), _ = s(c), _ && (_.c(), _.m(e.parentNode, e))), d[0] & /*progress*/
      128 && t !== (t = /*p*/
      c[41].unit + "") && fe(o, t);
    },
    d(c) {
      c && ($(e), $(o), $(l), $(a)), _.d(c);
    }
  };
}
function gs(n) {
  let e = rt(
    /*p*/
    n[41].index || 0
  ) + "", t;
  return {
    c() {
      t = z(e);
    },
    m(o, l) {
      L(o, t, l);
    },
    p(o, l) {
      l[0] & /*progress*/
      128 && e !== (e = rt(
        /*p*/
        o[41].index || 0
      ) + "") && fe(t, e);
    },
    d(o) {
      o && $(t);
    }
  };
}
function hs(n) {
  let e = rt(
    /*p*/
    n[41].index || 0
  ) + "", t, o, l = rt(
    /*p*/
    n[41].length
  ) + "", i;
  return {
    c() {
      t = z(e), o = z("/"), i = z(l);
    },
    m(a, r) {
      L(a, t, r), L(a, o, r), L(a, i, r);
    },
    p(a, r) {
      r[0] & /*progress*/
      128 && e !== (e = rt(
        /*p*/
        a[41].index || 0
      ) + "") && fe(t, e), r[0] & /*progress*/
      128 && l !== (l = rt(
        /*p*/
        a[41].length
      ) + "") && fe(i, l);
    },
    d(a) {
      a && ($(t), $(o), $(i));
    }
  };
}
function ko(n) {
  let e, t = (
    /*p*/
    n[41].index != null && Eo(n)
  );
  return {
    c() {
      t && t.c(), e = ct();
    },
    m(o, l) {
      t && t.m(o, l), L(o, e, l);
    },
    p(o, l) {
      /*p*/
      o[41].index != null ? t ? t.p(o, l) : (t = Eo(o), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(o) {
      o && $(e), t && t.d(o);
    }
  };
}
function Ao(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), o, l;
  return {
    c() {
      e = z(
        /*formatted_timer*/
        n[20]
      ), o = z(t), l = z("s");
    },
    m(i, a) {
      L(i, e, a), L(i, o, a), L(i, l, a);
    },
    p(i, a) {
      a[0] & /*formatted_timer*/
      1048576 && fe(
        e,
        /*formatted_timer*/
        i[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      i[0] ? `/${/*formatted_eta*/
      i[19]}` : "") && fe(o, t);
    },
    d(i) {
      i && ($(e), $(o), $(l));
    }
  };
}
function bs(n) {
  let e, t;
  return e = new ns({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      ol(e.$$.fragment);
    },
    m(o, l) {
      _l(e, o, l), t = !0;
    },
    p(o, l) {
      const i = {};
      l[0] & /*variant*/
      256 && (i.margin = /*variant*/
      o[8] === "default"), e.$set(i);
    },
    i(o) {
      t || (be(e.$$.fragment, o), t = !0);
    },
    o(o) {
      $e(e.$$.fragment, o), t = !1;
    },
    d(o) {
      il(e, o);
    }
  };
}
function vs(n) {
  let e, t, o, l, i, a = `${/*last_progress_level*/
  n[15] * 100}%`, r = (
    /*progress*/
    n[7] != null && yo(n)
  );
  return {
    c() {
      e = ye("div"), t = ye("div"), r && r.c(), o = _e(), l = ye("div"), i = ye("div"), ve(t, "class", "progress-level-inner svelte-v0wucf"), ve(i, "class", "progress-bar svelte-v0wucf"), Ie(i, "width", a), ve(l, "class", "progress-bar-wrap svelte-v0wucf"), ve(e, "class", "progress-level svelte-v0wucf");
    },
    m(s, _) {
      L(s, e, _), Ye(e, t), r && r.m(t, null), Ye(e, o), Ye(e, l), Ye(l, i), n[31](i);
    },
    p(s, _) {
      /*progress*/
      s[7] != null ? r ? r.p(s, _) : (r = yo(s), r.c(), r.m(t, null)) : r && (r.d(1), r = null), _[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      s[15] * 100}%`) && Ie(i, "width", a);
    },
    i: wn,
    o: wn,
    d(s) {
      s && $(e), r && r.d(), n[31](null);
    }
  };
}
function yo(n) {
  let e, t = jt(
    /*progress*/
    n[7]
  ), o = [];
  for (let l = 0; l < t.length; l += 1)
    o[l] = Oo(So(n, t, l));
  return {
    c() {
      for (let l = 0; l < o.length; l += 1)
        o[l].c();
      e = ct();
    },
    m(l, i) {
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(l, i);
      L(l, e, i);
    },
    p(l, i) {
      if (i[0] & /*progress_level, progress*/
      16512) {
        t = jt(
          /*progress*/
          l[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = So(l, t, a);
          o[a] ? o[a].p(r, i) : (o[a] = Oo(r), o[a].c(), o[a].m(e.parentNode, e));
        }
        for (; a < o.length; a += 1)
          o[a].d(1);
        o.length = t.length;
      }
    },
    d(l) {
      l && $(e), al(o, l);
    }
  };
}
function $o(n) {
  let e, t, o, l, i = (
    /*i*/
    n[43] !== 0 && ws()
  ), a = (
    /*p*/
    n[41].desc != null && Lo(n)
  ), r = (
    /*p*/
    n[41].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null && qo()
  ), s = (
    /*progress_level*/
    n[14] != null && Ro(n)
  );
  return {
    c() {
      i && i.c(), e = _e(), a && a.c(), t = _e(), r && r.c(), o = _e(), s && s.c(), l = ct();
    },
    m(_, c) {
      i && i.m(_, c), L(_, e, c), a && a.m(_, c), L(_, t, c), r && r.m(_, c), L(_, o, c), s && s.m(_, c), L(_, l, c);
    },
    p(_, c) {
      /*p*/
      _[41].desc != null ? a ? a.p(_, c) : (a = Lo(_), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), /*p*/
      _[41].desc != null && /*progress_level*/
      _[14] && /*progress_level*/
      _[14][
        /*i*/
        _[43]
      ] != null ? r || (r = qo(), r.c(), r.m(o.parentNode, o)) : r && (r.d(1), r = null), /*progress_level*/
      _[14] != null ? s ? s.p(_, c) : (s = Ro(_), s.c(), s.m(l.parentNode, l)) : s && (s.d(1), s = null);
    },
    d(_) {
      _ && ($(e), $(t), $(o), $(l)), i && i.d(_), a && a.d(_), r && r.d(_), s && s.d(_);
    }
  };
}
function ws(n) {
  let e;
  return {
    c() {
      e = z(" /");
    },
    m(t, o) {
      L(t, e, o);
    },
    d(t) {
      t && $(e);
    }
  };
}
function Lo(n) {
  let e = (
    /*p*/
    n[41].desc + ""
  ), t;
  return {
    c() {
      t = z(e);
    },
    m(o, l) {
      L(o, t, l);
    },
    p(o, l) {
      l[0] & /*progress*/
      128 && e !== (e = /*p*/
      o[41].desc + "") && fe(t, e);
    },
    d(o) {
      o && $(t);
    }
  };
}
function qo(n) {
  let e;
  return {
    c() {
      e = z("-");
    },
    m(t, o) {
      L(t, e, o);
    },
    d(t) {
      t && $(e);
    }
  };
}
function Ro(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[43]
  ] || 0)).toFixed(1) + "", t, o;
  return {
    c() {
      t = z(e), o = z("%");
    },
    m(l, i) {
      L(l, t, i), L(l, o, i);
    },
    p(l, i) {
      i[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (l[14][
        /*i*/
        l[43]
      ] || 0)).toFixed(1) + "") && fe(t, e);
    },
    d(l) {
      l && ($(t), $(o));
    }
  };
}
function Oo(n) {
  let e, t = (
    /*p*/
    (n[41].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null) && $o(n)
  );
  return {
    c() {
      t && t.c(), e = ct();
    },
    m(o, l) {
      t && t.m(o, l), L(o, e, l);
    },
    p(o, l) {
      /*p*/
      o[41].desc != null || /*progress_level*/
      o[14] && /*progress_level*/
      o[14][
        /*i*/
        o[43]
      ] != null ? t ? t.p(o, l) : (t = $o(o), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(o) {
      o && $(e), t && t.d(o);
    }
  };
}
function No(n) {
  let e, t, o, l;
  const i = (
    /*#slots*/
    n[30]["additional-loading-text"]
  ), a = ll(
    i,
    n,
    /*$$scope*/
    n[29],
    wo
  );
  return {
    c() {
      e = ye("p"), t = z(
        /*loading_text*/
        n[9]
      ), o = _e(), a && a.c(), ve(e, "class", "loading svelte-v0wucf");
    },
    m(r, s) {
      L(r, e, s), Ye(e, t), L(r, o, s), a && a.m(r, s), l = !0;
    },
    p(r, s) {
      (!l || s[0] & /*loading_text*/
      512) && fe(
        t,
        /*loading_text*/
        r[9]
      ), a && a.p && (!l || s[0] & /*$$scope*/
      536870912) && fl(
        a,
        i,
        r,
        /*$$scope*/
        r[29],
        l ? rl(
          i,
          /*$$scope*/
          r[29],
          s,
          fs
        ) : sl(
          /*$$scope*/
          r[29]
        ),
        wo
      );
    },
    i(r) {
      l || (be(a, r), l = !0);
    },
    o(r) {
      $e(a, r), l = !1;
    },
    d(r) {
      r && ($(e), $(o)), a && a.d(r);
    }
  };
}
function Ss(n) {
  let e, t, o, l, i;
  const a = [us, cs], r = [];
  function s(_, c) {
    return (
      /*status*/
      _[4] === "pending" ? 0 : (
        /*status*/
        _[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(n)) && (o = r[t] = a[t](n)), {
    c() {
      e = ye("div"), o && o.c(), ve(e, "class", l = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-v0wucf"), se(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), se(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), se(
        e,
        "generating",
        /*status*/
        n[4] === "generating" && /*show_progress*/
        n[6] === "full"
      ), se(
        e,
        "border",
        /*border*/
        n[12]
      ), Ie(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), Ie(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(_, c) {
      L(_, e, c), ~t && r[t].m(e, null), n[33](e), i = !0;
    },
    p(_, c) {
      let d = t;
      t = s(_), t === d ? ~t && r[t].p(_, c) : (o && (vn(), $e(r[d], 1, 1, () => {
        r[d] = null;
      }), bn()), ~t ? (o = r[t], o ? o.p(_, c) : (o = r[t] = a[t](_), o.c()), be(o, 1), o.m(e, null)) : o = null), (!i || c[0] & /*variant, show_progress*/
      320 && l !== (l = "wrap " + /*variant*/
      _[8] + " " + /*show_progress*/
      _[6] + " svelte-v0wucf")) && ve(e, "class", l), (!i || c[0] & /*variant, show_progress, status, show_progress*/
      336) && se(e, "hide", !/*status*/
      _[4] || /*status*/
      _[4] === "complete" || /*show_progress*/
      _[6] === "hidden"), (!i || c[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && se(
        e,
        "translucent",
        /*variant*/
        _[8] === "center" && /*status*/
        (_[4] === "pending" || /*status*/
        _[4] === "error") || /*translucent*/
        _[11] || /*show_progress*/
        _[6] === "minimal"
      ), (!i || c[0] & /*variant, show_progress, status, show_progress*/
      336) && se(
        e,
        "generating",
        /*status*/
        _[4] === "generating" && /*show_progress*/
        _[6] === "full"
      ), (!i || c[0] & /*variant, show_progress, border*/
      4416) && se(
        e,
        "border",
        /*border*/
        _[12]
      ), c[0] & /*absolute*/
      1024 && Ie(
        e,
        "position",
        /*absolute*/
        _[10] ? "absolute" : "static"
      ), c[0] & /*absolute*/
      1024 && Ie(
        e,
        "padding",
        /*absolute*/
        _[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(_) {
      i || (be(o), i = !0);
    },
    o(_) {
      $e(o), i = !1;
    },
    d(_) {
      _ && $(e), ~t && r[t].d(), n[33](null);
    }
  };
}
var Ts = function(n, e, t, o) {
  function l(i) {
    return i instanceof t ? i : new t(function(a) {
      a(i);
    });
  }
  return new (t || (t = Promise))(function(i, a) {
    function r(c) {
      try {
        _(o.next(c));
      } catch (d) {
        a(d);
      }
    }
    function s(c) {
      try {
        _(o.throw(c));
      } catch (d) {
        a(d);
      }
    }
    function _(c) {
      c.done ? i(c.value) : l(c.value).then(r, s);
    }
    _((o = o.apply(n, e || [])).next());
  });
};
let Mt = [], sn = !1;
function Cs(n) {
  return Ts(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (Mt.push(e), !sn) sn = !0;
      else return;
      yield as(), requestAnimationFrame(() => {
        let o = [0, 0];
        for (let l = 0; l < Mt.length; l++) {
          const a = Mt[l].getBoundingClientRect();
          (l === 0 || a.top + window.scrollY <= o[0]) && (o[0] = a.top + window.scrollY, o[1] = l);
        }
        window.scrollTo({ top: o[0] - 20, behavior: "smooth" }), sn = !1, Mt = [];
      });
    }
  });
}
function Es(n, e, t) {
  let o, { $$slots: l = {}, $$scope: i } = e;
  this && this.__awaiter;
  const a = rs();
  let { i18n: r } = e, { eta: s = null } = e, { queue_position: _ } = e, { queue_size: c } = e, { status: d } = e, { scroll_to_output: h = !1 } = e, { timer: b = !0 } = e, { show_progress: S = "full" } = e, { message: E = null } = e, { progress: A = null } = e, { variant: q = "default" } = e, { loading_text: g = "Loading..." } = e, { absolute: m = !0 } = e, { translucent: p = !1 } = e, { border: y = !1 } = e, { autoscroll: w } = e, N, P = !1, I = 0, W = 0, D = null, Y = null, R = 0, T = null, ie, ee = null, Fe = !0;
  const je = () => {
    t(0, s = t(27, D = t(19, F = null))), t(25, I = performance.now()), t(26, W = 0), P = !0, Xe();
  };
  function Xe() {
    requestAnimationFrame(() => {
      t(26, W = (performance.now() - I) / 1e3), P && Xe();
    });
  }
  function Ue() {
    t(26, W = 0), t(0, s = t(27, D = t(19, F = null))), P && (P = !1);
  }
  ss(() => {
    P && Ue();
  });
  let F = null;
  function Ze(u) {
    bo[u ? "unshift" : "push"](() => {
      ee = u, t(16, ee), t(7, A), t(14, T), t(15, ie);
    });
  }
  const H = () => {
    a("clear_status");
  };
  function Ke(u) {
    bo[u ? "unshift" : "push"](() => {
      N = u, t(13, N);
    });
  }
  return n.$$set = (u) => {
    "i18n" in u && t(1, r = u.i18n), "eta" in u && t(0, s = u.eta), "queue_position" in u && t(2, _ = u.queue_position), "queue_size" in u && t(3, c = u.queue_size), "status" in u && t(4, d = u.status), "scroll_to_output" in u && t(22, h = u.scroll_to_output), "timer" in u && t(5, b = u.timer), "show_progress" in u && t(6, S = u.show_progress), "message" in u && t(23, E = u.message), "progress" in u && t(7, A = u.progress), "variant" in u && t(8, q = u.variant), "loading_text" in u && t(9, g = u.loading_text), "absolute" in u && t(10, m = u.absolute), "translucent" in u && t(11, p = u.translucent), "border" in u && t(12, y = u.border), "autoscroll" in u && t(24, w = u.autoscroll), "$$scope" in u && t(29, i = u.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (s === null && t(0, s = D), s != null && D !== s && (t(28, Y = (performance.now() - I) / 1e3 + s), t(19, F = Y.toFixed(1)), t(27, D = s))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, R = Y === null || Y <= 0 || !W ? null : Math.min(W / Y, 1)), n.$$.dirty[0] & /*progress*/
    128 && A != null && t(18, Fe = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (A != null ? t(14, T = A.map((u) => {
      if (u.index != null && u.length != null)
        return u.index / u.length;
      if (u.progress != null)
        return u.progress;
    })) : t(14, T = null), T ? (t(15, ie = T[T.length - 1]), ee && (ie === 0 ? t(16, ee.style.transition = "0", ee) : t(16, ee.style.transition = "150ms", ee))) : t(15, ie = void 0)), n.$$.dirty[0] & /*status*/
    16 && (d === "pending" ? je() : Ue()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && N && h && (d === "pending" || d === "complete") && Cs(N, w), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, o = W.toFixed(1));
  }, [
    s,
    r,
    _,
    c,
    d,
    b,
    S,
    A,
    q,
    g,
    m,
    p,
    y,
    N,
    T,
    ie,
    ee,
    R,
    Fe,
    F,
    o,
    a,
    h,
    E,
    w,
    I,
    W,
    D,
    Y,
    i,
    l,
    Ze,
    H,
    Ke
  ];
}
class ks extends os {
  constructor(e) {
    super(), ls(
      this,
      e,
      Es,
      Ss,
      is,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
/*! @license DOMPurify 3.2.4 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.2.4/LICENSE */
const {
  entries: cl,
  setPrototypeOf: Do,
  isFrozen: As,
  getPrototypeOf: ys,
  getOwnPropertyDescriptor: $s
} = Object;
let {
  freeze: K,
  seal: ce,
  create: ul
} = Object, {
  apply: Sn,
  construct: Tn
} = typeof Reflect < "u" && Reflect;
K || (K = function(e) {
  return e;
});
ce || (ce = function(e) {
  return e;
});
Sn || (Sn = function(e, t, o) {
  return e.apply(t, o);
});
Tn || (Tn = function(e, t) {
  return new e(...t);
});
const It = J(Array.prototype.forEach), Ls = J(Array.prototype.lastIndexOf), Mo = J(Array.prototype.pop), ht = J(Array.prototype.push), qs = J(Array.prototype.splice), Bt = J(String.prototype.toLowerCase), rn = J(String.prototype.toString), Io = J(String.prototype.match), bt = J(String.prototype.replace), Rs = J(String.prototype.indexOf), Os = J(String.prototype.trim), he = J(Object.prototype.hasOwnProperty), Z = J(RegExp.prototype.test), vt = Ns(TypeError);
function J(n) {
  return function(e) {
    for (var t = arguments.length, o = new Array(t > 1 ? t - 1 : 0), l = 1; l < t; l++)
      o[l - 1] = arguments[l];
    return Sn(n, e, o);
  };
}
function Ns(n) {
  return function() {
    for (var e = arguments.length, t = new Array(e), o = 0; o < e; o++)
      t[o] = arguments[o];
    return Tn(n, t);
  };
}
function O(n, e) {
  let t = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : Bt;
  Do && Do(n, null);
  let o = e.length;
  for (; o--; ) {
    let l = e[o];
    if (typeof l == "string") {
      const i = t(l);
      i !== l && (As(e) || (e[o] = i), l = i);
    }
    n[l] = !0;
  }
  return n;
}
function Ds(n) {
  for (let e = 0; e < n.length; e++)
    he(n, e) || (n[e] = null);
  return n;
}
function Ge(n) {
  const e = ul(null);
  for (const [t, o] of cl(n))
    he(n, t) && (Array.isArray(o) ? e[t] = Ds(o) : o && typeof o == "object" && o.constructor === Object ? e[t] = Ge(o) : e[t] = o);
  return e;
}
function wt(n, e) {
  for (; n !== null; ) {
    const o = $s(n, e);
    if (o) {
      if (o.get)
        return J(o.get);
      if (typeof o.value == "function")
        return J(o.value);
    }
    n = ys(n);
  }
  function t() {
    return null;
  }
  return t;
}
const Po = K(["a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "big", "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "content", "data", "datalist", "dd", "decorator", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "marquee", "menu", "menuitem", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "shadow", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]), _n = K(["svg", "a", "altglyph", "altglyphdef", "altglyphitem", "animatecolor", "animatemotion", "animatetransform", "circle", "clippath", "defs", "desc", "ellipse", "filter", "font", "g", "glyph", "glyphref", "hkern", "image", "line", "lineargradient", "marker", "mask", "metadata", "mpath", "path", "pattern", "polygon", "polyline", "radialgradient", "rect", "stop", "style", "switch", "symbol", "text", "textpath", "title", "tref", "tspan", "view", "vkern"]), fn = K(["feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology", "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"]), Ms = K(["animate", "color-profile", "cursor", "discard", "font-face", "font-face-format", "font-face-name", "font-face-src", "font-face-uri", "foreignobject", "hatch", "hatchpath", "mesh", "meshgradient", "meshpatch", "meshrow", "missing-glyph", "script", "set", "solidcolor", "unknown", "use"]), cn = K(["math", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mspace", "msqrt", "mstyle", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "mprescripts"]), Is = K(["maction", "maligngroup", "malignmark", "mlongdiv", "mscarries", "mscarry", "msgroup", "mstack", "msline", "msrow", "semantics", "annotation", "annotation-xml", "mprescripts", "none"]), Fo = K(["#text"]), Uo = K(["accept", "action", "align", "alt", "autocapitalize", "autocomplete", "autopictureinpicture", "autoplay", "background", "bgcolor", "border", "capture", "cellpadding", "cellspacing", "checked", "cite", "class", "clear", "color", "cols", "colspan", "controls", "controlslist", "coords", "crossorigin", "datetime", "decoding", "default", "dir", "disabled", "disablepictureinpicture", "disableremoteplayback", "download", "draggable", "enctype", "enterkeyhint", "face", "for", "headers", "height", "hidden", "high", "href", "hreflang", "id", "inputmode", "integrity", "ismap", "kind", "label", "lang", "list", "loading", "loop", "low", "max", "maxlength", "media", "method", "min", "minlength", "multiple", "muted", "name", "nonce", "noshade", "novalidate", "nowrap", "open", "optimum", "pattern", "placeholder", "playsinline", "popover", "popovertarget", "popovertargetaction", "poster", "preload", "pubdate", "radiogroup", "readonly", "rel", "required", "rev", "reversed", "role", "rows", "rowspan", "spellcheck", "scope", "selected", "shape", "size", "sizes", "span", "srclang", "start", "src", "srcset", "step", "style", "summary", "tabindex", "title", "translate", "type", "usemap", "valign", "value", "width", "wrap", "xmlns", "slot"]), un = K(["accent-height", "accumulate", "additive", "alignment-baseline", "amplitude", "ascent", "attributename", "attributetype", "azimuth", "basefrequency", "baseline-shift", "begin", "bias", "by", "class", "clip", "clippathunits", "clip-path", "clip-rule", "color", "color-interpolation", "color-interpolation-filters", "color-profile", "color-rendering", "cx", "cy", "d", "dx", "dy", "diffuseconstant", "direction", "display", "divisor", "dur", "edgemode", "elevation", "end", "exponent", "fill", "fill-opacity", "fill-rule", "filter", "filterunits", "flood-color", "flood-opacity", "font-family", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "fx", "fy", "g1", "g2", "glyph-name", "glyphref", "gradientunits", "gradienttransform", "height", "href", "id", "image-rendering", "in", "in2", "intercept", "k", "k1", "k2", "k3", "k4", "kerning", "keypoints", "keysplines", "keytimes", "lang", "lengthadjust", "letter-spacing", "kernelmatrix", "kernelunitlength", "lighting-color", "local", "marker-end", "marker-mid", "marker-start", "markerheight", "markerunits", "markerwidth", "maskcontentunits", "maskunits", "max", "mask", "media", "method", "mode", "min", "name", "numoctaves", "offset", "operator", "opacity", "order", "orient", "orientation", "origin", "overflow", "paint-order", "path", "pathlength", "patterncontentunits", "patterntransform", "patternunits", "points", "preservealpha", "preserveaspectratio", "primitiveunits", "r", "rx", "ry", "radius", "refx", "refy", "repeatcount", "repeatdur", "restart", "result", "rotate", "scale", "seed", "shape-rendering", "slope", "specularconstant", "specularexponent", "spreadmethod", "startoffset", "stddeviation", "stitchtiles", "stop-color", "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke", "stroke-width", "style", "surfacescale", "systemlanguage", "tabindex", "tablevalues", "targetx", "targety", "transform", "transform-origin", "text-anchor", "text-decoration", "text-rendering", "textlength", "type", "u1", "u2", "unicode", "values", "viewbox", "visibility", "version", "vert-adv-y", "vert-origin-x", "vert-origin-y", "width", "word-spacing", "wrap", "writing-mode", "xchannelselector", "ychannelselector", "x", "x1", "x2", "xmlns", "y", "y1", "y2", "z", "zoomandpan"]), zo = K(["accent", "accentunder", "align", "bevelled", "close", "columnsalign", "columnlines", "columnspan", "denomalign", "depth", "dir", "display", "displaystyle", "encoding", "fence", "frame", "height", "href", "id", "largeop", "length", "linethickness", "lspace", "lquote", "mathbackground", "mathcolor", "mathsize", "mathvariant", "maxsize", "minsize", "movablelimits", "notation", "numalign", "open", "rowalign", "rowlines", "rowspacing", "rowspan", "rspace", "rquote", "scriptlevel", "scriptminsize", "scriptsizemultiplier", "selection", "separator", "separators", "stretchy", "subscriptshift", "supscriptshift", "symmetric", "voffset", "width", "xmlns"]), Pt = K(["xlink:href", "xml:id", "xlink:title", "xml:space", "xmlns:xlink"]), Ps = ce(/\{\{[\w\W]*|[\w\W]*\}\}/gm), Fs = ce(/<%[\w\W]*|[\w\W]*%>/gm), Us = ce(/\$\{[\w\W]*/gm), zs = ce(/^data-[\-\w.\u00B7-\uFFFF]+$/), Hs = ce(/^aria-[\-\w]+$/), dl = ce(
  /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  // eslint-disable-line no-useless-escape
), Bs = ce(/^(?:\w+script|data):/i), Gs = ce(
  /[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g
  // eslint-disable-line no-control-regex
), ml = ce(/^html$/i), Ws = ce(/^[a-z][.\w]*(-[.\w]+)+$/i);
var Ho = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  ARIA_ATTR: Hs,
  ATTR_WHITESPACE: Gs,
  CUSTOM_ELEMENT: Ws,
  DATA_ATTR: zs,
  DOCTYPE_NAME: ml,
  ERB_EXPR: Fs,
  IS_ALLOWED_URI: dl,
  IS_SCRIPT_OR_DATA: Bs,
  MUSTACHE_EXPR: Ps,
  TMPLIT_EXPR: Us
});
const St = {
  element: 1,
  text: 3,
  // Deprecated
  progressingInstruction: 7,
  comment: 8,
  document: 9
}, Vs = function() {
  return typeof window > "u" ? null : window;
}, Ys = function(e, t) {
  if (typeof e != "object" || typeof e.createPolicy != "function")
    return null;
  let o = null;
  const l = "data-tt-policy-suffix";
  t && t.hasAttribute(l) && (o = t.getAttribute(l));
  const i = "dompurify" + (o ? "#" + o : "");
  try {
    return e.createPolicy(i, {
      createHTML(a) {
        return a;
      },
      createScriptURL(a) {
        return a;
      }
    });
  } catch {
    return console.warn("TrustedTypes policy " + i + " could not be created."), null;
  }
}, Bo = function() {
  return {
    afterSanitizeAttributes: [],
    afterSanitizeElements: [],
    afterSanitizeShadowDOM: [],
    beforeSanitizeAttributes: [],
    beforeSanitizeElements: [],
    beforeSanitizeShadowDOM: [],
    uponSanitizeAttribute: [],
    uponSanitizeElement: [],
    uponSanitizeShadowNode: []
  };
};
function pl() {
  let n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : Vs();
  const e = (k) => pl(k);
  if (e.version = "3.2.4", e.removed = [], !n || !n.document || n.document.nodeType !== St.document || !n.Element)
    return e.isSupported = !1, e;
  let {
    document: t
  } = n;
  const o = t, l = o.currentScript, {
    DocumentFragment: i,
    HTMLTemplateElement: a,
    Node: r,
    Element: s,
    NodeFilter: _,
    NamedNodeMap: c = n.NamedNodeMap || n.MozNamedAttrMap,
    HTMLFormElement: d,
    DOMParser: h,
    trustedTypes: b
  } = n, S = s.prototype, E = wt(S, "cloneNode"), A = wt(S, "remove"), q = wt(S, "nextSibling"), g = wt(S, "childNodes"), m = wt(S, "parentNode");
  if (typeof a == "function") {
    const k = t.createElement("template");
    k.content && k.content.ownerDocument && (t = k.content.ownerDocument);
  }
  let p, y = "";
  const {
    implementation: w,
    createNodeIterator: N,
    createDocumentFragment: P,
    getElementsByTagName: I
  } = t, {
    importNode: W
  } = o;
  let D = Bo();
  e.isSupported = typeof cl == "function" && typeof m == "function" && w && w.createHTMLDocument !== void 0;
  const {
    MUSTACHE_EXPR: Y,
    ERB_EXPR: R,
    TMPLIT_EXPR: T,
    DATA_ATTR: ie,
    ARIA_ATTR: ee,
    IS_SCRIPT_OR_DATA: Fe,
    ATTR_WHITESPACE: je,
    CUSTOM_ELEMENT: Xe
  } = Ho;
  let {
    IS_ALLOWED_URI: Ue
  } = Ho, F = null;
  const Ze = O({}, [...Po, ..._n, ...fn, ...cn, ...Fo]);
  let H = null;
  const Ke = O({}, [...Uo, ...un, ...zo, ...Pt]);
  let u = Object.seal(ul(null, {
    tagNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    attributeNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    allowCustomizedBuiltInElements: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: !1
    }
  })), B = null, ae = null, ze = !0, ut = !0, Oe = !1, He = !0, Ne = !1, dt = !0, ue = !1, de = !1, Be = !1, Je = !1, kt = !1, At = !1, $n = !0, Ln = !1;
  const gl = "user-content-";
  let Xt = !0, mt = !1, Qe = {}, xe = null;
  const qn = O({}, ["annotation-xml", "audio", "colgroup", "desc", "foreignobject", "head", "iframe", "math", "mi", "mn", "mo", "ms", "mtext", "noembed", "noframes", "noscript", "plaintext", "script", "style", "svg", "template", "thead", "title", "video", "xmp"]);
  let Rn = null;
  const On = O({}, ["audio", "video", "img", "source", "image", "track"]);
  let Zt = null;
  const Nn = O({}, ["alt", "class", "for", "id", "label", "name", "pattern", "placeholder", "role", "summary", "title", "value", "style", "xmlns"]), yt = "http://www.w3.org/1998/Math/MathML", $t = "http://www.w3.org/2000/svg", Le = "http://www.w3.org/1999/xhtml";
  let et = Le, Kt = !1, Jt = null;
  const hl = O({}, [yt, $t, Le], rn);
  let Lt = O({}, ["mi", "mo", "mn", "ms", "mtext"]), qt = O({}, ["annotation-xml"]);
  const bl = O({}, ["title", "style", "font", "a", "script"]);
  let pt = null;
  const vl = ["application/xhtml+xml", "text/html"], wl = "text/html";
  let G = null, tt = null;
  const Sl = t.createElement("form"), Dn = function(f) {
    return f instanceof RegExp || f instanceof Function;
  }, Qt = function() {
    let f = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    if (!(tt && tt === f)) {
      if ((!f || typeof f != "object") && (f = {}), f = Ge(f), pt = // eslint-disable-next-line unicorn/prefer-includes
      vl.indexOf(f.PARSER_MEDIA_TYPE) === -1 ? wl : f.PARSER_MEDIA_TYPE, G = pt === "application/xhtml+xml" ? rn : Bt, F = he(f, "ALLOWED_TAGS") ? O({}, f.ALLOWED_TAGS, G) : Ze, H = he(f, "ALLOWED_ATTR") ? O({}, f.ALLOWED_ATTR, G) : Ke, Jt = he(f, "ALLOWED_NAMESPACES") ? O({}, f.ALLOWED_NAMESPACES, rn) : hl, Zt = he(f, "ADD_URI_SAFE_ATTR") ? O(Ge(Nn), f.ADD_URI_SAFE_ATTR, G) : Nn, Rn = he(f, "ADD_DATA_URI_TAGS") ? O(Ge(On), f.ADD_DATA_URI_TAGS, G) : On, xe = he(f, "FORBID_CONTENTS") ? O({}, f.FORBID_CONTENTS, G) : qn, B = he(f, "FORBID_TAGS") ? O({}, f.FORBID_TAGS, G) : {}, ae = he(f, "FORBID_ATTR") ? O({}, f.FORBID_ATTR, G) : {}, Qe = he(f, "USE_PROFILES") ? f.USE_PROFILES : !1, ze = f.ALLOW_ARIA_ATTR !== !1, ut = f.ALLOW_DATA_ATTR !== !1, Oe = f.ALLOW_UNKNOWN_PROTOCOLS || !1, He = f.ALLOW_SELF_CLOSE_IN_ATTR !== !1, Ne = f.SAFE_FOR_TEMPLATES || !1, dt = f.SAFE_FOR_XML !== !1, ue = f.WHOLE_DOCUMENT || !1, Je = f.RETURN_DOM || !1, kt = f.RETURN_DOM_FRAGMENT || !1, At = f.RETURN_TRUSTED_TYPE || !1, Be = f.FORCE_BODY || !1, $n = f.SANITIZE_DOM !== !1, Ln = f.SANITIZE_NAMED_PROPS || !1, Xt = f.KEEP_CONTENT !== !1, mt = f.IN_PLACE || !1, Ue = f.ALLOWED_URI_REGEXP || dl, et = f.NAMESPACE || Le, Lt = f.MATHML_TEXT_INTEGRATION_POINTS || Lt, qt = f.HTML_INTEGRATION_POINTS || qt, u = f.CUSTOM_ELEMENT_HANDLING || {}, f.CUSTOM_ELEMENT_HANDLING && Dn(f.CUSTOM_ELEMENT_HANDLING.tagNameCheck) && (u.tagNameCheck = f.CUSTOM_ELEMENT_HANDLING.tagNameCheck), f.CUSTOM_ELEMENT_HANDLING && Dn(f.CUSTOM_ELEMENT_HANDLING.attributeNameCheck) && (u.attributeNameCheck = f.CUSTOM_ELEMENT_HANDLING.attributeNameCheck), f.CUSTOM_ELEMENT_HANDLING && typeof f.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements == "boolean" && (u.allowCustomizedBuiltInElements = f.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements), Ne && (ut = !1), kt && (Je = !0), Qe && (F = O({}, Fo), H = [], Qe.html === !0 && (O(F, Po), O(H, Uo)), Qe.svg === !0 && (O(F, _n), O(H, un), O(H, Pt)), Qe.svgFilters === !0 && (O(F, fn), O(H, un), O(H, Pt)), Qe.mathMl === !0 && (O(F, cn), O(H, zo), O(H, Pt))), f.ADD_TAGS && (F === Ze && (F = Ge(F)), O(F, f.ADD_TAGS, G)), f.ADD_ATTR && (H === Ke && (H = Ge(H)), O(H, f.ADD_ATTR, G)), f.ADD_URI_SAFE_ATTR && O(Zt, f.ADD_URI_SAFE_ATTR, G), f.FORBID_CONTENTS && (xe === qn && (xe = Ge(xe)), O(xe, f.FORBID_CONTENTS, G)), Xt && (F["#text"] = !0), ue && O(F, ["html", "head", "body"]), F.table && (O(F, ["tbody"]), delete B.tbody), f.TRUSTED_TYPES_POLICY) {
        if (typeof f.TRUSTED_TYPES_POLICY.createHTML != "function")
          throw vt('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');
        if (typeof f.TRUSTED_TYPES_POLICY.createScriptURL != "function")
          throw vt('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');
        p = f.TRUSTED_TYPES_POLICY, y = p.createHTML("");
      } else
        p === void 0 && (p = Ys(b, l)), p !== null && typeof y == "string" && (y = p.createHTML(""));
      K && K(f), tt = f;
    }
  }, Mn = O({}, [..._n, ...fn, ...Ms]), In = O({}, [...cn, ...Is]), Tl = function(f) {
    let v = m(f);
    (!v || !v.tagName) && (v = {
      namespaceURI: et,
      tagName: "template"
    });
    const C = Bt(f.tagName), U = Bt(v.tagName);
    return Jt[f.namespaceURI] ? f.namespaceURI === $t ? v.namespaceURI === Le ? C === "svg" : v.namespaceURI === yt ? C === "svg" && (U === "annotation-xml" || Lt[U]) : !!Mn[C] : f.namespaceURI === yt ? v.namespaceURI === Le ? C === "math" : v.namespaceURI === $t ? C === "math" && qt[U] : !!In[C] : f.namespaceURI === Le ? v.namespaceURI === $t && !qt[U] || v.namespaceURI === yt && !Lt[U] ? !1 : !In[C] && (bl[C] || !Mn[C]) : !!(pt === "application/xhtml+xml" && Jt[f.namespaceURI]) : !1;
  }, we = function(f) {
    ht(e.removed, {
      element: f
    });
    try {
      m(f).removeChild(f);
    } catch {
      A(f);
    }
  }, Rt = function(f, v) {
    try {
      ht(e.removed, {
        attribute: v.getAttributeNode(f),
        from: v
      });
    } catch {
      ht(e.removed, {
        attribute: null,
        from: v
      });
    }
    if (v.removeAttribute(f), f === "is")
      if (Je || kt)
        try {
          we(v);
        } catch {
        }
      else
        try {
          v.setAttribute(f, "");
        } catch {
        }
  }, Pn = function(f) {
    let v = null, C = null;
    if (Be)
      f = "<remove></remove>" + f;
    else {
      const V = Io(f, /^[\r\n\t ]+/);
      C = V && V[0];
    }
    pt === "application/xhtml+xml" && et === Le && (f = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>' + f + "</body></html>");
    const U = p ? p.createHTML(f) : f;
    if (et === Le)
      try {
        v = new h().parseFromString(U, pt);
      } catch {
      }
    if (!v || !v.documentElement) {
      v = w.createDocument(et, "template", null);
      try {
        v.documentElement.innerHTML = Kt ? y : U;
      } catch {
      }
    }
    const j = v.body || v.documentElement;
    return f && C && j.insertBefore(t.createTextNode(C), j.childNodes[0] || null), et === Le ? I.call(v, ue ? "html" : "body")[0] : ue ? v.documentElement : j;
  }, Fn = function(f) {
    return N.call(
      f.ownerDocument || f,
      f,
      // eslint-disable-next-line no-bitwise
      _.SHOW_ELEMENT | _.SHOW_COMMENT | _.SHOW_TEXT | _.SHOW_PROCESSING_INSTRUCTION | _.SHOW_CDATA_SECTION,
      null
    );
  }, xt = function(f) {
    return f instanceof d && (typeof f.nodeName != "string" || typeof f.textContent != "string" || typeof f.removeChild != "function" || !(f.attributes instanceof c) || typeof f.removeAttribute != "function" || typeof f.setAttribute != "function" || typeof f.namespaceURI != "string" || typeof f.insertBefore != "function" || typeof f.hasChildNodes != "function");
  }, Un = function(f) {
    return typeof r == "function" && f instanceof r;
  };
  function qe(k, f, v) {
    It(k, (C) => {
      C.call(e, f, v, tt);
    });
  }
  const zn = function(f) {
    let v = null;
    if (qe(D.beforeSanitizeElements, f, null), xt(f))
      return we(f), !0;
    const C = G(f.nodeName);
    if (qe(D.uponSanitizeElement, f, {
      tagName: C,
      allowedTags: F
    }), f.hasChildNodes() && !Un(f.firstElementChild) && Z(/<[/\w]/g, f.innerHTML) && Z(/<[/\w]/g, f.textContent) || f.nodeType === St.progressingInstruction || dt && f.nodeType === St.comment && Z(/<[/\w]/g, f.data))
      return we(f), !0;
    if (!F[C] || B[C]) {
      if (!B[C] && Bn(C) && (u.tagNameCheck instanceof RegExp && Z(u.tagNameCheck, C) || u.tagNameCheck instanceof Function && u.tagNameCheck(C)))
        return !1;
      if (Xt && !xe[C]) {
        const U = m(f) || f.parentNode, j = g(f) || f.childNodes;
        if (j && U) {
          const V = j.length;
          for (let Q = V - 1; Q >= 0; --Q) {
            const Se = E(j[Q], !0);
            Se.__removalCount = (f.__removalCount || 0) + 1, U.insertBefore(Se, q(f));
          }
        }
      }
      return we(f), !0;
    }
    return f instanceof s && !Tl(f) || (C === "noscript" || C === "noembed" || C === "noframes") && Z(/<\/no(script|embed|frames)/i, f.innerHTML) ? (we(f), !0) : (Ne && f.nodeType === St.text && (v = f.textContent, It([Y, R, T], (U) => {
      v = bt(v, U, " ");
    }), f.textContent !== v && (ht(e.removed, {
      element: f.cloneNode()
    }), f.textContent = v)), qe(D.afterSanitizeElements, f, null), !1);
  }, Hn = function(f, v, C) {
    if ($n && (v === "id" || v === "name") && (C in t || C in Sl))
      return !1;
    if (!(ut && !ae[v] && Z(ie, v))) {
      if (!(ze && Z(ee, v))) {
        if (!H[v] || ae[v]) {
          if (
            // First condition does a very basic check if a) it's basically a valid custom element tagname AND
            // b) if the tagName passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            // and c) if the attribute name passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.attributeNameCheck
            !(Bn(f) && (u.tagNameCheck instanceof RegExp && Z(u.tagNameCheck, f) || u.tagNameCheck instanceof Function && u.tagNameCheck(f)) && (u.attributeNameCheck instanceof RegExp && Z(u.attributeNameCheck, v) || u.attributeNameCheck instanceof Function && u.attributeNameCheck(v)) || // Alternative, second condition checks if it's an `is`-attribute, AND
            // the value passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            v === "is" && u.allowCustomizedBuiltInElements && (u.tagNameCheck instanceof RegExp && Z(u.tagNameCheck, C) || u.tagNameCheck instanceof Function && u.tagNameCheck(C)))
          ) return !1;
        } else if (!Zt[v]) {
          if (!Z(Ue, bt(C, je, ""))) {
            if (!((v === "src" || v === "xlink:href" || v === "href") && f !== "script" && Rs(C, "data:") === 0 && Rn[f])) {
              if (!(Oe && !Z(Fe, bt(C, je, "")))) {
                if (C)
                  return !1;
              }
            }
          }
        }
      }
    }
    return !0;
  }, Bn = function(f) {
    return f !== "annotation-xml" && Io(f, Xe);
  }, Gn = function(f) {
    qe(D.beforeSanitizeAttributes, f, null);
    const {
      attributes: v
    } = f;
    if (!v || xt(f))
      return;
    const C = {
      attrName: "",
      attrValue: "",
      keepAttr: !0,
      allowedAttributes: H,
      forceKeepAttr: void 0
    };
    let U = v.length;
    for (; U--; ) {
      const j = v[U], {
        name: V,
        namespaceURI: Q,
        value: Se
      } = j, gt = G(V);
      let X = V === "value" ? Se : Os(Se);
      if (C.attrName = gt, C.attrValue = X, C.keepAttr = !0, C.forceKeepAttr = void 0, qe(D.uponSanitizeAttribute, f, C), X = C.attrValue, Ln && (gt === "id" || gt === "name") && (Rt(V, f), X = gl + X), dt && Z(/((--!?|])>)|<\/(style|title)/i, X)) {
        Rt(V, f);
        continue;
      }
      if (C.forceKeepAttr || (Rt(V, f), !C.keepAttr))
        continue;
      if (!He && Z(/\/>/i, X)) {
        Rt(V, f);
        continue;
      }
      Ne && It([Y, R, T], (Vn) => {
        X = bt(X, Vn, " ");
      });
      const Wn = G(f.nodeName);
      if (Hn(Wn, gt, X)) {
        if (p && typeof b == "object" && typeof b.getAttributeType == "function" && !Q)
          switch (b.getAttributeType(Wn, gt)) {
            case "TrustedHTML": {
              X = p.createHTML(X);
              break;
            }
            case "TrustedScriptURL": {
              X = p.createScriptURL(X);
              break;
            }
          }
        try {
          Q ? f.setAttributeNS(Q, V, X) : f.setAttribute(V, X), xt(f) ? we(f) : Mo(e.removed);
        } catch {
        }
      }
    }
    qe(D.afterSanitizeAttributes, f, null);
  }, Cl = function k(f) {
    let v = null;
    const C = Fn(f);
    for (qe(D.beforeSanitizeShadowDOM, f, null); v = C.nextNode(); )
      qe(D.uponSanitizeShadowNode, v, null), zn(v), Gn(v), v.content instanceof i && k(v.content);
    qe(D.afterSanitizeShadowDOM, f, null);
  };
  return e.sanitize = function(k) {
    let f = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}, v = null, C = null, U = null, j = null;
    if (Kt = !k, Kt && (k = "<!-->"), typeof k != "string" && !Un(k))
      if (typeof k.toString == "function") {
        if (k = k.toString(), typeof k != "string")
          throw vt("dirty is not a string, aborting");
      } else
        throw vt("toString is not a function");
    if (!e.isSupported)
      return k;
    if (de || Qt(f), e.removed = [], typeof k == "string" && (mt = !1), mt) {
      if (k.nodeName) {
        const Se = G(k.nodeName);
        if (!F[Se] || B[Se])
          throw vt("root node is forbidden and cannot be sanitized in-place");
      }
    } else if (k instanceof r)
      v = Pn("<!---->"), C = v.ownerDocument.importNode(k, !0), C.nodeType === St.element && C.nodeName === "BODY" || C.nodeName === "HTML" ? v = C : v.appendChild(C);
    else {
      if (!Je && !Ne && !ue && // eslint-disable-next-line unicorn/prefer-includes
      k.indexOf("<") === -1)
        return p && At ? p.createHTML(k) : k;
      if (v = Pn(k), !v)
        return Je ? null : At ? y : "";
    }
    v && Be && we(v.firstChild);
    const V = Fn(mt ? k : v);
    for (; U = V.nextNode(); )
      zn(U), Gn(U), U.content instanceof i && Cl(U.content);
    if (mt)
      return k;
    if (Je) {
      if (kt)
        for (j = P.call(v.ownerDocument); v.firstChild; )
          j.appendChild(v.firstChild);
      else
        j = v;
      return (H.shadowroot || H.shadowrootmode) && (j = W.call(o, j, !0)), j;
    }
    let Q = ue ? v.outerHTML : v.innerHTML;
    return ue && F["!doctype"] && v.ownerDocument && v.ownerDocument.doctype && v.ownerDocument.doctype.name && Z(ml, v.ownerDocument.doctype.name) && (Q = "<!DOCTYPE " + v.ownerDocument.doctype.name + `>
` + Q), Ne && It([Y, R, T], (Se) => {
      Q = bt(Q, Se, " ");
    }), p && At ? p.createHTML(Q) : Q;
  }, e.setConfig = function() {
    let k = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    Qt(k), de = !0;
  }, e.clearConfig = function() {
    tt = null, de = !1;
  }, e.isValidAttribute = function(k, f, v) {
    tt || Qt({});
    const C = G(k), U = G(f);
    return Hn(C, U, v);
  }, e.addHook = function(k, f) {
    typeof f == "function" && ht(D[k], f);
  }, e.removeHook = function(k, f) {
    if (f !== void 0) {
      const v = Ls(D[k], f);
      return v === -1 ? void 0 : qs(D[k], v, 1)[0];
    }
    return Mo(D[k]);
  }, e.removeHooks = function(k) {
    D[k] = [];
  }, e.removeAllHooks = function() {
    D = Bo();
  }, e;
}
pl();
const {
  SvelteComponent: ah,
  add_render_callback: sh,
  append: rh,
  attr: _h,
  bubble: fh,
  check_outros: ch,
  create_component: uh,
  create_in_transition: dh,
  create_out_transition: mh,
  destroy_component: ph,
  detach: gh,
  element: hh,
  group_outros: bh,
  init: vh,
  insert: wh,
  listen: Sh,
  mount_component: Th,
  run_all: Ch,
  safe_not_equal: Eh,
  set_data: kh,
  space: Ah,
  stop_propagation: yh,
  text: $h,
  toggle_class: Lh,
  transition_in: qh,
  transition_out: Rh
} = window.__gradio__svelte__internal, { createEventDispatcher: Oh, onMount: Nh } = window.__gradio__svelte__internal, {
  SvelteComponent: Dh,
  append: Mh,
  attr: Ih,
  bubble: Ph,
  check_outros: Fh,
  create_animation: Uh,
  create_component: zh,
  destroy_component: Hh,
  detach: Bh,
  element: Gh,
  ensure_array_like: Wh,
  fix_and_outro_and_destroy_block: Vh,
  fix_position: Yh,
  group_outros: jh,
  init: Xh,
  insert: Zh,
  mount_component: Kh,
  noop: Jh,
  safe_not_equal: Qh,
  set_style: xh,
  space: eb,
  transition_in: tb,
  transition_out: nb,
  update_keyed_each: ob
} = window.__gradio__svelte__internal, {
  SvelteComponent: js,
  add_flush_callback: Go,
  assign: Xs,
  bind: Wo,
  binding_callbacks: Vo,
  create_component: Cn,
  destroy_component: En,
  detach: Zs,
  get_spread_object: Ks,
  get_spread_update: Js,
  init: Qs,
  insert: xs,
  mount_component: kn,
  safe_not_equal: er,
  space: tr,
  transition_in: An,
  transition_out: yn
} = window.__gradio__svelte__internal;
function nr(n) {
  let e, t, o, l, i, a;
  const r = [
    {
      autoscroll: (
        /*gradio*/
        n[16].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      n[16].i18n
    ) },
    /*loading_status*/
    n[14]
  ];
  let s = {};
  for (let h = 0; h < r.length; h += 1)
    s = Xs(s, r[h]);
  e = new ks({ props: s }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    n[18]
  );
  function _(h) {
    n[19](h);
  }
  function c(h) {
    n[20](h);
  }
  let d = {
    choices: (
      /*choices*/
      n[8]
    ),
    max_choices: (
      /*max_choices*/
      n[7]
    ),
    label: (
      /*label*/
      n[2]
    ),
    info: (
      /*info*/
      n[3]
    ),
    show_label: (
      /*show_label*/
      n[9]
    ),
    allow_custom_value: (
      /*allow_custom_value*/
      n[15]
    ),
    filterable: (
      /*filterable*/
      n[10]
    ),
    container: (
      /*container*/
      n[11]
    ),
    i18n: (
      /*gradio*/
      n[16].i18n
    ),
    disabled: !/*interactive*/
    n[17]
  };
  return (
    /*value*/
    n[0] !== void 0 && (d.value = /*value*/
    n[0]), /*value_is_output*/
    n[1] !== void 0 && (d.value_is_output = /*value_is_output*/
    n[1]), o = new Ya({ props: d }), Vo.push(() => Wo(o, "value", _)), Vo.push(() => Wo(o, "value_is_output", c)), o.$on(
      "change",
      /*change_handler*/
      n[21]
    ), o.$on(
      "input",
      /*input_handler*/
      n[22]
    ), o.$on(
      "select",
      /*select_handler*/
      n[23]
    ), o.$on(
      "blur",
      /*blur_handler*/
      n[24]
    ), o.$on(
      "focus",
      /*focus_handler*/
      n[25]
    ), o.$on(
      "key_up",
      /*key_up_handler*/
      n[26]
    ), {
      c() {
        Cn(e.$$.fragment), t = tr(), Cn(o.$$.fragment);
      },
      m(h, b) {
        kn(e, h, b), xs(h, t, b), kn(o, h, b), a = !0;
      },
      p(h, b) {
        const S = b & /*gradio, loading_status*/
        81920 ? Js(r, [
          b & /*gradio*/
          65536 && {
            autoscroll: (
              /*gradio*/
              h[16].autoscroll
            )
          },
          b & /*gradio*/
          65536 && { i18n: (
            /*gradio*/
            h[16].i18n
          ) },
          b & /*loading_status*/
          16384 && Ks(
            /*loading_status*/
            h[14]
          )
        ]) : {};
        e.$set(S);
        const E = {};
        b & /*choices*/
        256 && (E.choices = /*choices*/
        h[8]), b & /*max_choices*/
        128 && (E.max_choices = /*max_choices*/
        h[7]), b & /*label*/
        4 && (E.label = /*label*/
        h[2]), b & /*info*/
        8 && (E.info = /*info*/
        h[3]), b & /*show_label*/
        512 && (E.show_label = /*show_label*/
        h[9]), b & /*allow_custom_value*/
        32768 && (E.allow_custom_value = /*allow_custom_value*/
        h[15]), b & /*filterable*/
        1024 && (E.filterable = /*filterable*/
        h[10]), b & /*container*/
        2048 && (E.container = /*container*/
        h[11]), b & /*gradio*/
        65536 && (E.i18n = /*gradio*/
        h[16].i18n), b & /*interactive*/
        131072 && (E.disabled = !/*interactive*/
        h[17]), !l && b & /*value*/
        1 && (l = !0, E.value = /*value*/
        h[0], Go(() => l = !1)), !i && b & /*value_is_output*/
        2 && (i = !0, E.value_is_output = /*value_is_output*/
        h[1], Go(() => i = !1)), o.$set(E);
      },
      i(h) {
        a || (An(e.$$.fragment, h), An(o.$$.fragment, h), a = !0);
      },
      o(h) {
        yn(e.$$.fragment, h), yn(o.$$.fragment, h), a = !1;
      },
      d(h) {
        h && Zs(t), En(e, h), En(o, h);
      }
    }
  );
}
function or(n) {
  let e, t;
  return e = new Ul({
    props: {
      visible: (
        /*visible*/
        n[6]
      ),
      elem_id: (
        /*elem_id*/
        n[4]
      ),
      elem_classes: (
        /*elem_classes*/
        n[5]
      ),
      padding: (
        /*container*/
        n[11]
      ),
      allow_overflow: !1,
      scale: (
        /*scale*/
        n[12]
      ),
      min_width: (
        /*min_width*/
        n[13]
      ),
      $$slots: { default: [nr] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Cn(e.$$.fragment);
    },
    m(o, l) {
      kn(e, o, l), t = !0;
    },
    p(o, [l]) {
      const i = {};
      l & /*visible*/
      64 && (i.visible = /*visible*/
      o[6]), l & /*elem_id*/
      16 && (i.elem_id = /*elem_id*/
      o[4]), l & /*elem_classes*/
      32 && (i.elem_classes = /*elem_classes*/
      o[5]), l & /*container*/
      2048 && (i.padding = /*container*/
      o[11]), l & /*scale*/
      4096 && (i.scale = /*scale*/
      o[12]), l & /*min_width*/
      8192 && (i.min_width = /*min_width*/
      o[13]), l & /*$$scope, choices, max_choices, label, info, show_label, allow_custom_value, filterable, container, gradio, interactive, value, value_is_output, loading_status*/
      134467471 && (i.$$scope = { dirty: l, ctx: o }), e.$set(i);
    },
    i(o) {
      t || (An(e.$$.fragment, o), t = !0);
    },
    o(o) {
      yn(e.$$.fragment, o), t = !1;
    },
    d(o) {
      En(e, o);
    }
  };
}
function lr(n, e, t) {
  let { label: o = "Dropdown" } = e, { info: l = void 0 } = e, { elem_id: i = "" } = e, { elem_classes: a = [] } = e, { visible: r = !0 } = e, { value: s = void 0 } = e, { value_is_output: _ = !1 } = e, { max_choices: c = null } = e, { choices: d } = e, { show_label: h } = e, { filterable: b } = e, { container: S = !0 } = e, { scale: E = null } = e, { min_width: A = void 0 } = e, { loading_status: q } = e, { allow_custom_value: g = !1 } = e, { gradio: m } = e, { interactive: p } = e;
  const y = () => m.dispatch("clear_status", q);
  function w(T) {
    s = T, t(0, s);
  }
  function N(T) {
    _ = T, t(1, _);
  }
  const P = () => m.dispatch("change"), I = () => m.dispatch("input"), W = (T) => m.dispatch("select", T.detail), D = () => m.dispatch("blur"), Y = () => m.dispatch("focus"), R = () => m.dispatch("key_up");
  return n.$$set = (T) => {
    "label" in T && t(2, o = T.label), "info" in T && t(3, l = T.info), "elem_id" in T && t(4, i = T.elem_id), "elem_classes" in T && t(5, a = T.elem_classes), "visible" in T && t(6, r = T.visible), "value" in T && t(0, s = T.value), "value_is_output" in T && t(1, _ = T.value_is_output), "max_choices" in T && t(7, c = T.max_choices), "choices" in T && t(8, d = T.choices), "show_label" in T && t(9, h = T.show_label), "filterable" in T && t(10, b = T.filterable), "container" in T && t(11, S = T.container), "scale" in T && t(12, E = T.scale), "min_width" in T && t(13, A = T.min_width), "loading_status" in T && t(14, q = T.loading_status), "allow_custom_value" in T && t(15, g = T.allow_custom_value), "gradio" in T && t(16, m = T.gradio), "interactive" in T && t(17, p = T.interactive);
  }, [
    s,
    _,
    o,
    l,
    i,
    a,
    r,
    c,
    d,
    h,
    b,
    S,
    E,
    A,
    q,
    g,
    m,
    p,
    y,
    w,
    N,
    P,
    I,
    W,
    D,
    Y,
    R
  ];
}
class lb extends js {
  constructor(e) {
    super(), Qs(this, e, lr, or, er, {
      label: 2,
      info: 3,
      elem_id: 4,
      elem_classes: 5,
      visible: 6,
      value: 0,
      value_is_output: 1,
      max_choices: 7,
      choices: 8,
      show_label: 9,
      filterable: 10,
      container: 11,
      scale: 12,
      min_width: 13,
      loading_status: 14,
      allow_custom_value: 15,
      gradio: 16,
      interactive: 17
    });
  }
}
export {
  Ya as BaseMultiselect,
  lb as default
};
