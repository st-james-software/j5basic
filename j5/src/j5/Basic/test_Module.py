#!/usr/bin/env python

from j5.Basic import Module

class TestModule:
    def test_resolve(self):
        assert Module.resolvemodule("j5.Basic.Module") == Module
        from j5.Config import ConfigTree
        assert Module.resolvemodule("j5.Config.ConfigTree.Node") == ConfigTree.Node
