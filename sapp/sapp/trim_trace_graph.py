#!/usr/bin/env python3

import logging
from typing import Tuple

from sapp.pipeline import PipelineStep, Summary
from sapp.trace_graph import TraceGraph
from sapp.trimmed_trace_graph import TrimmedTraceGraph


log = logging.getLogger()


class TrimTraceGraph(PipelineStep[TraceGraph, TraceGraph]):
    def run(
        self, input: TraceGraph, summary: Summary = None
    ) -> Tuple[TraceGraph, Summary]:
        self.summary = summary or {}

        if self.summary.get("affected_files") is None:
            self.summary["graph"] = input  # used by ranker
            return input, self.summary

        log.info("Trimming graph to affected files.")
        trimmed_graph = TrimmedTraceGraph(
            self.summary["affected_files"], self.summary.get("affected_issues_only")
        )
        trimmed_graph.populate_from_trace_graph(input)

        self.summary["graph"] = trimmed_graph  # used by ranker
        return trimmed_graph, self.summary
