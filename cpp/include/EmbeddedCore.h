#pragma once
#include <stdint.h>
#include <stddef.h>
namespace lord_sumi {
enum class RunStatus { Success, Failure, Cancelled, Skipped, Invalid };
struct PipelineSnapshot { uint32_t total, success, failure, cancelled, skipped; uint64_t duration_ms; bool fault; };
class PipelineHealth {
 public:
  PipelineHealth(): state_{0,0,0,0,0,0,false}, last_end_(0), started_(false) {}
  bool ingest(uint64_t started_ms,uint64_t ended_ms,RunStatus status) {
    if(state_.fault) return false;
    if(ended_ms<started_ms || (started_ && started_ms<last_end_) ||
       status==RunStatus::Invalid || state_.total==UINT32_MAX ||
       UINT64_MAX-state_.duration_ms<ended_ms-started_ms) { state_.fault=true; return false; }
    ++state_.total;
    switch(status) {
      case RunStatus::Success: ++state_.success; break;
      case RunStatus::Failure: ++state_.failure; break;
      case RunStatus::Cancelled: ++state_.cancelled; break;
      case RunStatus::Skipped: ++state_.skipped; break;
      default: state_.fault=true; return false;
    }
    state_.duration_ms+=ended_ms-started_ms;
    last_end_=ended_ms; started_=true; return true;
  }
  PipelineSnapshot snapshot() const {return state_;}
  void reset(){state_={0,0,0,0,0,0,false};last_end_=0;started_=false;}
 private: PipelineSnapshot state_;uint64_t last_end_;bool started_;
};
}