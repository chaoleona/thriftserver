include "base.thrift"
namespace go hi
namespace py hi
struct HiRequest {
    1: string Name,
    255: optional base.Base Base,
}
struct HiResponse {
    1: string Resp,
    255: base.BaseResp BaseResp,
}
service HiService {
    HiResponse Hi(1: HiRequest req)
}
