import json
import sys


class JSONSchemaGenerator:
    def __init__(self):
        self.obj = None
        self.s = None

    def load(self, json_str):
        self.obj = json.loads(json_str)

    def schema(self, schema_str):
        self.s = json.loads(schema_str)

    def set_defaults (self, s):
        default = { }
        # if s != None:
        #     default['description'] = s['description']
        #     default['additionalProperties'] = s['additionalProperties']
        #     default['required'] = s['required']
        # else:
        #     default['description'] = 'Dummy description'
        #     default['additionalProperties'] = False
        #     default['required'] = True
        return default

    def _skemateDict(self, d, s):
        #print "_skemateDict"
        skema=self.set_defaults(s)
        skema['type'] = 'object'
        skema['properties'] = { }
        for key, value in d.items ():
            #print "key > ", key
            if s == None:
                new_s = None
            else:
                new_s = s['properties'][key]
            skema['properties'][key] = self._skemate(value, new_s)
        return skema

    def _skemateList(self, l, s):
        #print "_skemateList"
        skema=self.set_defaults(s)
        skema['type'] = 'array'
        skema['minItems'] = 0
        skema['items'] = self._skemate(l[0])
        return skema

    def _skemateStr(self, str, s):
        #print "_skemateStr"
        res=self.set_defaults(s)
        res['type'] = 'string'
        # res['pattern'] = ''
        # res['value'] = str
        return res

    def _skemateInt(self, i, s):
        #print "_skemateInt"
        res=self.set_defaults(s)
        res['type'] = 'integer'
        # res['pattern'] = ''
        # res['value'] = i
        return res

    def _skemateFloat(self, f, s):
        print("_skemateFloat")
        res=self.set_defaults(s)
        res['type'] = 'float'
        # res['pattern'] = ''
        # res['value'] = f
        return res

    def _skemateNone(self, f, s):
        print("_skemateNone")
        res=self.set_defaults(s)
        return res

    def _skemateBool(self, f, s):
        print("_skemateNone")
        res=self.set_defaults(s)
        res['type'] = 'boolean'
        return res

    def _skemate(self, o, s=None):
        ret = None
        if isinstance(o, (list, tuple)):
            ret = self._skemateList(o, s)
        elif isinstance(o, dict):
            ret = self._skemateDict(o, s)
        elif isinstance(o, str):
            ret = self._skemateStr(o, s)
        elif isinstance(o, int):
            ret = self._skemateInt(o, s)
        elif isinstance(o, float):
            ret = self._skemateFloat(o, s)
        elif o is None:
            ret = self._skemateNone(o, s)
        elif o is False or o is True:
            ret = self._skemateBool(o, s)
        return ret

    def generate(self):
        ret = self._skemate(self.obj, self.s)

        ret['required'] = []
        for prop in ret['properties']:
            ret['required'].append(prop)
        if 'icons' in ret['properties']:
            ret['properties']['icons']['required'] = []
            for prop in ret['properties']['icons']['properties']:
                ret['properties']['icons']['required'].append(prop)

        ret["$id"] = "https://example.com/entry-schema"
        ret["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        return ret