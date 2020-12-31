# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    Array,
    BaseClass,
    ClassDecl,
    DecltypeSpecifier,
    Field,
    ForwardDecl,
    Function,
    FunctionType,
    FundamentalSpecifier,
    Method,
    NameSpecifier,
    PQName,
    Parameter,
    Pointer,
    Reference,
    TemplateArgument,
    TemplateDecl,
    TemplateNonTypeParam,
    TemplateSpecialization,
    TemplateTypeParam,
    Token,
    Type,
    Value,
    Variable,
)
from cxxheaderparser.simple import ClassScope, NamespaceScope, ParsedData, parse_string


def test_template_base_template_ns():
    content = """
      class A : public B<int, int>::C {};
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="A")], classkey="class"
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="B",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    FundamentalSpecifier(
                                                                        name="int"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    FundamentalSpecifier(
                                                                        name="int"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                ]
                                            ),
                                        ),
                                        NameSpecifier(name="C"),
                                    ]
                                ),
                            )
                        ],
                    )
                )
            ]
        )
    )


def test_template_non_type_various():
    content = """
      // simple non-type template parameter
      template <int N> struct S { int a[N]; };
      
      template <const char *> struct S2 {};
      
      // complicated non-type example
      template <char c,        // integral type
                int (&ra)[5],  // lvalue reference to object (of array type)
                int (*pf)(int) // pointer to function
                >
      struct Complicated {
        // calls the function selected at compile time
        // and stores the result in the array selected at compile time
        void foo(char base) { ra[4] = pf(c - base); }
      };
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="S")], classkey="struct"
                        ),
                        template=TemplateDecl(
                            params=[
                                TemplateNonTypeParam(
                                    type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    ),
                                    name="N",
                                )
                            ]
                        ),
                    ),
                    fields=[
                        Field(
                            name="a",
                            type=Array(
                                array_of=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="int")]
                                    )
                                ),
                                size=Value(tokens=[Token(value="N")]),
                            ),
                            access="public",
                        )
                    ],
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="S2")], classkey="struct"
                        ),
                        template=TemplateDecl(
                            params=[
                                TemplateNonTypeParam(
                                    type=Pointer(
                                        ptr_to=Type(
                                            typename=PQName(
                                                segments=[
                                                    FundamentalSpecifier(name="char")
                                                ]
                                            ),
                                            const=True,
                                        )
                                    )
                                )
                            ]
                        ),
                    )
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="Complicated")],
                            classkey="struct",
                        ),
                        template=TemplateDecl(
                            params=[
                                TemplateNonTypeParam(
                                    type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="char")]
                                        )
                                    ),
                                    name="c",
                                ),
                                TemplateNonTypeParam(
                                    type=Reference(
                                        ref_to=Array(
                                            array_of=Type(
                                                typename=PQName(
                                                    segments=[
                                                        FundamentalSpecifier(name="int")
                                                    ]
                                                )
                                            ),
                                            size=Value(tokens=[Token(value="5")]),
                                        )
                                    ),
                                    name="ra",
                                ),
                                TemplateNonTypeParam(
                                    type=Pointer(
                                        ptr_to=FunctionType(
                                            return_type=Type(
                                                typename=PQName(
                                                    segments=[
                                                        FundamentalSpecifier(name="int")
                                                    ]
                                                )
                                            ),
                                            parameters=[
                                                Parameter(
                                                    type=Type(
                                                        typename=PQName(
                                                            segments=[
                                                                FundamentalSpecifier(
                                                                    name="int"
                                                                )
                                                            ]
                                                        )
                                                    )
                                                )
                                            ],
                                        )
                                    ),
                                    name="pf",
                                ),
                            ]
                        ),
                    ),
                    methods=[
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="foo")]),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="char")]
                                        )
                                    ),
                                    name="base",
                                )
                            ],
                            has_body=True,
                            access="public",
                        )
                    ],
                ),
            ]
        )
    )


def test_template_dependent_nontype_default():
    content = """
      template <class T, typename T::type n = 0> class X;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            forward_decls=[
                ForwardDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name="X")], classkey="class"
                    ),
                    template=TemplateDecl(
                        params=[
                            TemplateTypeParam(typekey="class", name="T"),
                            TemplateNonTypeParam(
                                type=Type(
                                    typename=PQName(
                                        segments=[
                                            NameSpecifier(name="T"),
                                            NameSpecifier(name="type"),
                                        ]
                                    )
                                ),
                                name="n",
                                default=Value(tokens=[Token(value="0")]),
                            ),
                        ]
                    ),
                )
            ]
        )
    )


def test_template_optional_names():
    content = """
      template <class> class My_vector;
      template <class = void> struct My_op_functor;
      template <typename...> class My_tuple;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            forward_decls=[
                ForwardDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name="My_vector")], classkey="class"
                    ),
                    template=TemplateDecl(params=[TemplateTypeParam(typekey="class")]),
                ),
                ForwardDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name="My_op_functor")],
                        classkey="struct",
                    ),
                    template=TemplateDecl(
                        params=[
                            TemplateTypeParam(
                                typekey="class",
                                default=Value(tokens=[Token(value="void")]),
                            )
                        ]
                    ),
                ),
                ForwardDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name="My_tuple")], classkey="class"
                    ),
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="typename", param_pack=True)]
                    ),
                ),
            ]
        )
    )


def test_template_template_template():
    content = """
      template<typename T> struct eval; // primary template 
 
      template<template<typename, typename...> class TT, typename T1, typename... Rest>
      struct eval<TT<T1, Rest...>> {}; // partial specialization of eval
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[
                                NameSpecifier(
                                    name="eval",
                                    specialization=TemplateSpecialization(
                                        args=[
                                            TemplateArgument(
                                                arg=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(
                                                                name="TT",
                                                                specialization=TemplateSpecialization(
                                                                    args=[
                                                                        TemplateArgument(
                                                                            arg=Type(
                                                                                typename=PQName(
                                                                                    segments=[
                                                                                        NameSpecifier(
                                                                                            name="T1"
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            )
                                                                        ),
                                                                        TemplateArgument(
                                                                            arg=Type(
                                                                                typename=PQName(
                                                                                    segments=[
                                                                                        NameSpecifier(
                                                                                            name="Rest"
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ),
                                                                            param_pack=True,
                                                                        ),
                                                                    ]
                                                                ),
                                                            )
                                                        ]
                                                    )
                                                )
                                            )
                                        ]
                                    ),
                                )
                            ],
                            classkey="struct",
                        ),
                        template=TemplateDecl(
                            params=[
                                TemplateTypeParam(
                                    typekey="class",
                                    name="TT",
                                    template=TemplateDecl(
                                        params=[
                                            TemplateTypeParam(typekey="typename"),
                                            TemplateTypeParam(
                                                typekey="typename", param_pack=True
                                            ),
                                        ]
                                    ),
                                ),
                                TemplateTypeParam(typekey="typename", name="T1"),
                                TemplateTypeParam(
                                    typekey="typename", name="Rest", param_pack=True
                                ),
                            ]
                        ),
                    )
                )
            ],
            forward_decls=[
                ForwardDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name="eval")], classkey="struct"
                    ),
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="typename", name="T")]
                    ),
                )
            ],
        )
    )


def test_template_static_var():
    content = """
      template <typename T>
      struct X {
        static int x;
      };

      template <typename T>
      int X<T>::x = 5;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="X")], classkey="struct"
                        ),
                        template=TemplateDecl(
                            params=[TemplateTypeParam(typekey="typename", name="T")]
                        ),
                    ),
                    fields=[
                        Field(
                            access="public",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name="x",
                            static=True,
                        )
                    ],
                )
            ],
            variables=[
                Variable(
                    name=PQName(
                        segments=[
                            NameSpecifier(
                                name="X",
                                specialization=TemplateSpecialization(
                                    args=[
                                        TemplateArgument(
                                            arg=Type(
                                                typename=PQName(
                                                    segments=[NameSpecifier(name="T")]
                                                )
                                            )
                                        )
                                    ]
                                ),
                            ),
                            NameSpecifier(name="x"),
                        ]
                    ),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    value=Value(tokens=[Token(value="5")]),
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="typename", name="T")]
                    ),
                )
            ],
        )
    )


def test_template_fn_template():
    content = """
      class S {
        template <typename Allocator> StringRef copy(Allocator &A) const {
          // Don't request a length 0 copy from the allocator.
          if (empty())
            return StringRef();
          char *S = A.template Allocate<char>(Length);
          std::copy(begin(), end(), S);
          return StringRef(S, Length);
        }
      };
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="S")], classkey="class"
                        )
                    ),
                    methods=[
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[NameSpecifier(name="StringRef")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="copy")]),
                            parameters=[
                                Parameter(
                                    type=Reference(
                                        ref_to=Type(
                                            typename=PQName(
                                                segments=[
                                                    NameSpecifier(name="Allocator")
                                                ]
                                            )
                                        )
                                    ),
                                    name="A",
                                )
                            ],
                            has_body=True,
                            template=TemplateDecl(
                                params=[
                                    TemplateTypeParam(
                                        typekey="typename", name="Allocator"
                                    )
                                ]
                            ),
                            access="private",
                            const=True,
                        )
                    ],
                )
            ]
        )
    )


def test_template_fn_param_initializer():
    content = """
      template <typename T, typename U>
      void fn(something<T, U> s = something<T, U>{1, 2, 3});
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn")]),
                    parameters=[
                        Parameter(
                            type=Type(
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="something",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="T"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="U"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                ]
                                            ),
                                        )
                                    ]
                                )
                            ),
                            name="s",
                            default=Value(
                                tokens=[
                                    Token(value="something"),
                                    Token(value="<"),
                                    Token(value="T"),
                                    Token(value=","),
                                    Token(value="U"),
                                    Token(value=">"),
                                    Token(value="{"),
                                    Token(value="1"),
                                    Token(value=","),
                                    Token(value="2"),
                                    Token(value=","),
                                    Token(value="3"),
                                    Token(value="}"),
                                ]
                            ),
                        )
                    ],
                    template=TemplateDecl(
                        params=[
                            TemplateTypeParam(typekey="typename", name="T"),
                            TemplateTypeParam(typekey="typename", name="U"),
                        ]
                    ),
                )
            ]
        )
    )


def test_template_huge():
    content = """
      // clang-format off
      class AlmondClass
      {
      public:
          std::map<unsigned, std::pair<unsigned, SnailTemplateClass<SnailNamespace::SnailClass> > > meth(bool flag,
                  std::map<unsigned, std::pair<unsigned, SnailTemplateClass<SnailNamespace::SnailClass> > > bigArg);
      };
      
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="AlmondClass")],
                            classkey="class",
                        )
                    ),
                    methods=[
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(name="std"),
                                        NameSpecifier(
                                            name="map",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    FundamentalSpecifier(
                                                                        name="unsigned"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="std"
                                                                    ),
                                                                    NameSpecifier(
                                                                        name="pair",
                                                                        specialization=TemplateSpecialization(
                                                                            args=[
                                                                                TemplateArgument(
                                                                                    arg=Type(
                                                                                        typename=PQName(
                                                                                            segments=[
                                                                                                FundamentalSpecifier(
                                                                                                    name="unsigned"
                                                                                                )
                                                                                            ]
                                                                                        )
                                                                                    )
                                                                                ),
                                                                                TemplateArgument(
                                                                                    arg=Type(
                                                                                        typename=PQName(
                                                                                            segments=[
                                                                                                NameSpecifier(
                                                                                                    name="SnailTemplateClass",
                                                                                                    specialization=TemplateSpecialization(
                                                                                                        args=[
                                                                                                            TemplateArgument(
                                                                                                                arg=Type(
                                                                                                                    typename=PQName(
                                                                                                                        segments=[
                                                                                                                            NameSpecifier(
                                                                                                                                name="SnailNamespace"
                                                                                                                            ),
                                                                                                                            NameSpecifier(
                                                                                                                                name="SnailClass"
                                                                                                                            ),
                                                                                                                        ]
                                                                                                                    )
                                                                                                                )
                                                                                                            )
                                                                                                        ]
                                                                                                    ),
                                                                                                )
                                                                                            ]
                                                                                        )
                                                                                    )
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    ),
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="meth")]),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="bool")]
                                        )
                                    ),
                                    name="flag",
                                ),
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                NameSpecifier(name="std"),
                                                NameSpecifier(
                                                    name="map",
                                                    specialization=TemplateSpecialization(
                                                        args=[
                                                            TemplateArgument(
                                                                arg=Type(
                                                                    typename=PQName(
                                                                        segments=[
                                                                            FundamentalSpecifier(
                                                                                name="unsigned"
                                                                            )
                                                                        ]
                                                                    )
                                                                )
                                                            ),
                                                            TemplateArgument(
                                                                arg=Type(
                                                                    typename=PQName(
                                                                        segments=[
                                                                            NameSpecifier(
                                                                                name="std"
                                                                            ),
                                                                            NameSpecifier(
                                                                                name="pair",
                                                                                specialization=TemplateSpecialization(
                                                                                    args=[
                                                                                        TemplateArgument(
                                                                                            arg=Type(
                                                                                                typename=PQName(
                                                                                                    segments=[
                                                                                                        FundamentalSpecifier(
                                                                                                            name="unsigned"
                                                                                                        )
                                                                                                    ]
                                                                                                )
                                                                                            )
                                                                                        ),
                                                                                        TemplateArgument(
                                                                                            arg=Type(
                                                                                                typename=PQName(
                                                                                                    segments=[
                                                                                                        NameSpecifier(
                                                                                                            name="SnailTemplateClass",
                                                                                                            specialization=TemplateSpecialization(
                                                                                                                args=[
                                                                                                                    TemplateArgument(
                                                                                                                        arg=Type(
                                                                                                                            typename=PQName(
                                                                                                                                segments=[
                                                                                                                                    NameSpecifier(
                                                                                                                                        name="SnailNamespace"
                                                                                                                                    ),
                                                                                                                                    NameSpecifier(
                                                                                                                                        name="SnailClass"
                                                                                                                                    ),
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        )
                                                                                                                    )
                                                                                                                ]
                                                                                                            ),
                                                                                                        )
                                                                                                    ]
                                                                                                )
                                                                                            )
                                                                                        ),
                                                                                    ]
                                                                                ),
                                                                            ),
                                                                        ]
                                                                    )
                                                                )
                                                            ),
                                                        ]
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                    name="bigArg",
                                ),
                            ],
                            access="public",
                        )
                    ],
                )
            ]
        )
    )


def test_template_specialized():
    content = """
      template <> class FruitFly<int> : public Fly {};
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[
                                NameSpecifier(
                                    name="FruitFly",
                                    specialization=TemplateSpecialization(
                                        args=[
                                            TemplateArgument(
                                                arg=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            FundamentalSpecifier(
                                                                name="int"
                                                            )
                                                        ]
                                                    )
                                                )
                                            )
                                        ]
                                    ),
                                )
                            ],
                            classkey="class",
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(segments=[NameSpecifier(name="Fly")]),
                            )
                        ],
                        template=TemplateDecl(),
                    )
                )
            ]
        )
    )


def test_template_class_defaults():
    content = """
      template <typename VALUE, typename VALUE_SET_ITERATOR,
                typename ACCESSOR = Raddish::SimpleAccessor<VALUE, VALUE_SET_ITERATOR>>
      class Raddish_SetIterator : public Raddish_Iterator<VALUE> {
      protected:
        VALUE_SET_ITERATOR _beg, _end;
      
      public:
        Raddish_SetIterator(const VALUE_SET_ITERATOR &begin,
                            const VALUE_SET_ITERATOR &end) {
          init(begin, end);
        }
      };
      
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="Raddish_SetIterator")],
                            classkey="class",
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="Raddish_Iterator",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="VALUE"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    )
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                        template=TemplateDecl(
                            params=[
                                TemplateTypeParam(typekey="typename", name="VALUE"),
                                TemplateTypeParam(
                                    typekey="typename", name="VALUE_SET_ITERATOR"
                                ),
                                TemplateTypeParam(
                                    typekey="typename",
                                    name="ACCESSOR",
                                    default=Value(
                                        tokens=[
                                            Token(value="Raddish"),
                                            Token(value="::"),
                                            Token(value="SimpleAccessor"),
                                            Token(value="<"),
                                            Token(value="VALUE"),
                                            Token(value=","),
                                            Token(value="VALUE_SET_ITERATOR"),
                                            Token(value=">"),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    fields=[
                        Field(
                            access="protected",
                            type=Type(
                                typename=PQName(
                                    segments=[NameSpecifier(name="VALUE_SET_ITERATOR")]
                                )
                            ),
                            name="_beg",
                        ),
                        Field(
                            access="protected",
                            type=Type(
                                typename=PQName(
                                    segments=[NameSpecifier(name="VALUE_SET_ITERATOR")]
                                )
                            ),
                            name="_end",
                        ),
                    ],
                    methods=[
                        Method(
                            return_type=None,
                            name=PQName(
                                segments=[NameSpecifier(name="Raddish_SetIterator")]
                            ),
                            parameters=[
                                Parameter(
                                    type=Reference(
                                        ref_to=Type(
                                            typename=PQName(
                                                segments=[
                                                    NameSpecifier(
                                                        name="VALUE_SET_ITERATOR"
                                                    )
                                                ]
                                            ),
                                            const=True,
                                        )
                                    ),
                                    name="begin",
                                ),
                                Parameter(
                                    type=Reference(
                                        ref_to=Type(
                                            typename=PQName(
                                                segments=[
                                                    NameSpecifier(
                                                        name="VALUE_SET_ITERATOR"
                                                    )
                                                ]
                                            ),
                                            const=True,
                                        )
                                    ),
                                    name="end",
                                ),
                            ],
                            has_body=True,
                            access="public",
                            constructor=True,
                        )
                    ],
                )
            ]
        )
    )


def test_template_many_packs():
    content = """
      // clang-format off
      
      template <typename Type>
      class XYZ : public MyBaseClass<Type, int>
      {
          public:
          XYZ();
      };
      
      template <typename ValueT, typename... IterTs>
      class concat_iterator
          : public iterator_facade_base<concat_iterator<ValueT, IterTs...>,
                                        std::forward_iterator_tag, ValueT> {
      };
      
      template <std::size_t N, std::size_t... I>
      struct build_index_impl : build_index_impl<N - 1, N - 1, I...> {};
      
      template <std::size_t... I>
      struct build_index_impl<0, I...> : index_sequence<I...> {};
      
      template <typename F, typename P, typename... T>
      struct is_callable<F, P, typelist<T...>,
              void_t<decltype(((*std::declval<P>()).*std::declval<F>())(std::declval<T>()...))>>
          : std::true_type {};
      
      template <typename T...>
      struct S : public T... {};
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="XYZ")], classkey="class"
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="MyBaseClass",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="Type"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    FundamentalSpecifier(
                                                                        name="int"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                        template=TemplateDecl(
                            params=[TemplateTypeParam(typekey="typename", name="Type")]
                        ),
                    ),
                    methods=[
                        Method(
                            return_type=None,
                            name=PQName(segments=[NameSpecifier(name="XYZ")]),
                            parameters=[],
                            access="public",
                            constructor=True,
                        )
                    ],
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="concat_iterator")],
                            classkey="class",
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="iterator_facade_base",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="concat_iterator",
                                                                        specialization=TemplateSpecialization(
                                                                            args=[
                                                                                TemplateArgument(
                                                                                    arg=Type(
                                                                                        typename=PQName(
                                                                                            segments=[
                                                                                                NameSpecifier(
                                                                                                    name="ValueT"
                                                                                                )
                                                                                            ]
                                                                                        )
                                                                                    )
                                                                                ),
                                                                                TemplateArgument(
                                                                                    arg=Type(
                                                                                        typename=PQName(
                                                                                            segments=[
                                                                                                NameSpecifier(
                                                                                                    name="IterTs"
                                                                                                )
                                                                                            ]
                                                                                        )
                                                                                    ),
                                                                                    param_pack=True,
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="std"
                                                                    ),
                                                                    NameSpecifier(
                                                                        name="forward_iterator_tag"
                                                                    ),
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="ValueT"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                        template=TemplateDecl(
                            params=[
                                TemplateTypeParam(typekey="typename", name="ValueT"),
                                TemplateTypeParam(
                                    typekey="typename", name="IterTs", param_pack=True
                                ),
                            ]
                        ),
                    )
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="build_index_impl")],
                            classkey="struct",
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="build_index_impl",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Value(
                                                            tokens=[
                                                                Token(value="N"),
                                                                Token(value="-"),
                                                                Token(value="1"),
                                                            ]
                                                        )
                                                    ),
                                                    TemplateArgument(
                                                        arg=Value(
                                                            tokens=[
                                                                Token(value="N"),
                                                                Token(value="-"),
                                                                Token(value="1"),
                                                            ]
                                                        )
                                                    ),
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="I"
                                                                    )
                                                                ]
                                                            )
                                                        ),
                                                        param_pack=True,
                                                    ),
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                        template=TemplateDecl(
                            params=[
                                TemplateNonTypeParam(
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                NameSpecifier(name="std"),
                                                NameSpecifier(name="size_t"),
                                            ]
                                        )
                                    ),
                                    name="N",
                                ),
                                TemplateNonTypeParam(
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                NameSpecifier(name="std"),
                                                NameSpecifier(name="size_t"),
                                            ]
                                        )
                                    ),
                                    name="I",
                                    param_pack=True,
                                ),
                            ]
                        ),
                    )
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[
                                NameSpecifier(
                                    name="build_index_impl",
                                    specialization=TemplateSpecialization(
                                        args=[
                                            TemplateArgument(
                                                arg=Value(tokens=[Token(value="0")])
                                            ),
                                            TemplateArgument(
                                                arg=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(name="I")
                                                        ]
                                                    )
                                                ),
                                                param_pack=True,
                                            ),
                                        ]
                                    ),
                                )
                            ],
                            classkey="struct",
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="index_sequence",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="I"
                                                                    )
                                                                ]
                                                            )
                                                        ),
                                                        param_pack=True,
                                                    )
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                        template=TemplateDecl(
                            params=[
                                TemplateNonTypeParam(
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                NameSpecifier(name="std"),
                                                NameSpecifier(name="size_t"),
                                            ]
                                        )
                                    ),
                                    name="I",
                                    param_pack=True,
                                )
                            ]
                        ),
                    )
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[
                                NameSpecifier(
                                    name="is_callable",
                                    specialization=TemplateSpecialization(
                                        args=[
                                            TemplateArgument(
                                                arg=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(name="F")
                                                        ]
                                                    )
                                                )
                                            ),
                                            TemplateArgument(
                                                arg=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(name="P")
                                                        ]
                                                    )
                                                )
                                            ),
                                            TemplateArgument(
                                                arg=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(
                                                                name="typelist",
                                                                specialization=TemplateSpecialization(
                                                                    args=[
                                                                        TemplateArgument(
                                                                            arg=Type(
                                                                                typename=PQName(
                                                                                    segments=[
                                                                                        NameSpecifier(
                                                                                            name="T"
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ),
                                                                            param_pack=True,
                                                                        )
                                                                    ]
                                                                ),
                                                            )
                                                        ]
                                                    )
                                                )
                                            ),
                                            TemplateArgument(
                                                arg=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(
                                                                name="void_t",
                                                                specialization=TemplateSpecialization(
                                                                    args=[
                                                                        TemplateArgument(
                                                                            arg=Type(
                                                                                typename=PQName(
                                                                                    segments=[
                                                                                        DecltypeSpecifier(
                                                                                            tokens=[
                                                                                                Token(
                                                                                                    value="("
                                                                                                ),
                                                                                                Token(
                                                                                                    value="("
                                                                                                ),
                                                                                                Token(
                                                                                                    value="*"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="std"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="::"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="declval"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="<"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="P"
                                                                                                ),
                                                                                                Token(
                                                                                                    value=">"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="("
                                                                                                ),
                                                                                                Token(
                                                                                                    value=")"
                                                                                                ),
                                                                                                Token(
                                                                                                    value=")"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="."
                                                                                                ),
                                                                                                Token(
                                                                                                    value="*"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="std"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="::"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="declval"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="<"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="F"
                                                                                                ),
                                                                                                Token(
                                                                                                    value=">"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="("
                                                                                                ),
                                                                                                Token(
                                                                                                    value=")"
                                                                                                ),
                                                                                                Token(
                                                                                                    value=")"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="("
                                                                                                ),
                                                                                                Token(
                                                                                                    value="std"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="::"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="declval"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="<"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="T"
                                                                                                ),
                                                                                                Token(
                                                                                                    value=">"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="("
                                                                                                ),
                                                                                                Token(
                                                                                                    value=")"
                                                                                                ),
                                                                                                Token(
                                                                                                    value="..."
                                                                                                ),
                                                                                                Token(
                                                                                                    value=")"
                                                                                                ),
                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            )
                                                                        )
                                                                    ]
                                                                ),
                                                            )
                                                        ]
                                                    )
                                                )
                                            ),
                                        ]
                                    ),
                                )
                            ],
                            classkey="struct",
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(name="std"),
                                        NameSpecifier(name="true_type"),
                                    ]
                                ),
                            )
                        ],
                        template=TemplateDecl(
                            params=[
                                TemplateTypeParam(typekey="typename", name="F"),
                                TemplateTypeParam(typekey="typename", name="P"),
                                TemplateTypeParam(
                                    typekey="typename", name="T", param_pack=True
                                ),
                            ]
                        ),
                    )
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="S")], classkey="struct"
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(segments=[NameSpecifier(name="T")]),
                                param_pack=True,
                            )
                        ],
                        template=TemplateDecl(
                            params=[
                                TemplateNonTypeParam(
                                    type=Type(
                                        typename=PQName(
                                            segments=[NameSpecifier(name="T")]
                                        )
                                    ),
                                    param_pack=True,
                                )
                            ]
                        ),
                    )
                ),
            ]
        )
    )
