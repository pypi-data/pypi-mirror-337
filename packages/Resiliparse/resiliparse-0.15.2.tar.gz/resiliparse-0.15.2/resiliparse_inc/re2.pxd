from libc.stdint cimport int64_t
from libcpp.map cimport map
from libcpp.string cimport string
from libcpp.vector cimport vector
from resiliparse_inc.string_view cimport string_view


cdef extern from "<re2/re2.h>" namespace "re2::Options" nogil:
    cdef enum Encoding:
        EncodingUTF8,
        EncodingLatin1


cdef extern from "<re2/re2.h>" namespace "re2::RE2" nogil:
    cdef enum ErrorCode:
        NoError = 0,
        ErrorInternal,
        ErrorBadEscape,
        ErrorBadCharClass,
        ErrorBadCharRange,
        ErrorMissingBracket,
        ErrorMissingParen,
        ErrorUnexpectedParen,
        ErrorTrailingBackslash,
        ErrorRepeatArgument,
        ErrorRepeatSize,
        ErrorRepeatOp,
        ErrorBadPerlOp,
        ErrorBadUTF8,
        ErrorBadNamedCapture,
        ErrorPatternTooLarge

    enum Anchor:
        UNANCHORED,
        ANCHOR_START,
        ANCHOR_BOTH

    cdef cppclass Options:
        Options()

        Encoding encoding() const
        void set_encoding(Encoding encoding)

        bint posix_syntax() const
        void set_posix_syntax(bint b)

        bint longest_match() const
        void set_longest_match(bint b)

        bint log_errors() const
        void set_log_errors(bint b)

        int64_t max_mem() const
        void set_max_mem(int64_t m)

        bint literal() const
        void set_literal(bint b)

        bint never_nl() const
        void set_never_nl(bint b)

        bint dot_nl() const
        void set_dot_nl(bint b)

        bint never_capture() const
        void set_never_capture(bint b)

        bint case_sensitive() const
        void set_case_sensitive(bint b)

        bint perl_classes() const
        void set_perl_classes(bint b)

        bint word_boundary() const
        void set_word_boundary(bint b)

        bint one_line() const
        void set_one_line(bint b)

        void Copy(const Options& src)
        int ParseFlags() const


cdef extern from "<re2/re2.h>" namespace "re2" nogil:
    cdef cppclass RE2:
        bint ok() const
        const string& pattern() const
        const string& error() const
        ErrorCode error_code() const
        const string& error_arg() const

        int ProgramSize() const
        int ReverseProgramSize() const

        int ProgramFanout(vector[int]* histogram) const
        int ReverseProgramFanout(vector[int]* histogram) const

        PossibleMatchRange(string* min, string* max, int maxlen) const
        int NumberOfCapturingGroups() const
        const map[string, int]& NamedCapturingGroups() const
        const map[int, string]& CapturingGroupNames() const

        bint Match(const string_view text, size_t startpos, size_t endpos, Anchor re_anchor,
                   string_view* submatch, int nsubmatch) const
        bint CheckRewriteString(const string_view rewrite, string* error) const
        bint Rewrite(string* out, const string_view rewrite, const string_view* vec, int veclen) const


cdef extern from "<re2/re2.h>" namespace "re2::RE2" nogil:
    cdef cppclass Arg

    bint FullMatchN(const string_view text, const RE2& re, const Arg* const args[], int n)
    bint PartialMatchN(const string_view text, const RE2& re, const Arg* const args[], int n)
    bint ConsumeN(string_view* input, const RE2& re, const Arg* const args[], int n)
    bint FindAndConsumeN(string_view* input, const RE2& re, const Arg* const args[], int n)

    bint FullMatch(const string_view text, const RE2& re)
    bint PartialMatch(const string_view text, const RE2& re)
    bint Consume(string_view* input, const RE2& re)
    bint FindAndConsume(string_view* input, const RE2& re)

    bint Replace(string* str, const RE2& re, const string_view rewrite)
    int GlobalReplace(string* str, const RE2& re, const string_view rewrite)
    bint Extract(const string_view text, const RE2& re, const string_view rewrite, string* out)
    string QuoteMeta(const string_view unquoted)
    int MaxSubmatch(const string_view rewrite)


# Stack assignable wrapper (Cython 0.29.x doesn't support cpp_locals yet)
cdef extern from * nogil:
    """
    #include <string_view>

    class RE2Stack {
    public:
        RE2Stack()
            : instance(nullptr) {}
        RE2Stack(const char* pattern)
            : instance(new re2::RE2(pattern)) {}
        RE2Stack(const std::string& pattern)
            : instance(new re2::RE2(pattern)){}
        RE2Stack(const std::string_view pattern)
            : instance(new re2::RE2(pattern)) {}
        RE2Stack(const std::string_view pattern, const re2::RE2::Options& options)
            : instance(new re2::RE2(pattern, options)) {}
        RE2Stack(const RE2Stack&) = delete;
        RE2Stack(RE2Stack&&) = delete;
        ~RE2Stack() {
            if (instance) {
                delete instance;
                instance = nullptr;
            }
        }
        RE2Stack& operator=(const RE2Stack&) = delete;
        RE2Stack& operator=(RE2Stack&& other) {
            if (this != &other) {
                instance = other.instance;
                other.instance = nullptr;
            }
            return *this;
        }

        inline const re2::RE2& operator()() const {
            return *instance;
        }

    private:
        re2::RE2* instance;
    };
    """
    cdef cppclass RE2Stack:
        RE2Stack()
        RE2Stack(const char* pattern)
        RE2Stack(const string& pattern)
        RE2Stack(const string_view pattern)
        RE2Stack(const string&, const Options& options)
        RE2Stack(const char* pattern, const Options& options)
        RE2Stack(const string_view pattern, const Options& options)

        inline const RE2& operator()() const
