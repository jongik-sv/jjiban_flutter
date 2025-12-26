import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';

void main() {
  runApp(const ClaudeViewerApp());
}

class ClaudeViewerApp extends StatelessWidget {
  const ClaudeViewerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Claude Viewer',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF1E1E1E),
      ),
      home: const TerminalScreen(),
    );
  }
}

class TerminalScreen extends StatefulWidget {
  const TerminalScreen({super.key});

  @override
  State<TerminalScreen> createState() => _TerminalScreenState();
}

class _TerminalScreenState extends State<TerminalScreen> {
  final TextEditingController _promptController = TextEditingController();
  final TextEditingController _inputController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final FocusNode _inputFocusNode = FocusNode();

  final StringBuffer _outputBuffer = StringBuffer();
  Process? _process;
  bool _isRunning = false;
  String _status = 'Ready';

  @override
  void initState() {
    super.initState();
    _promptController.text = './hello 폴더에 간단한 hello world html 페이지 하나만 만들어줘';
  }

  @override
  void dispose() {
    _promptController.dispose();
    _inputController.dispose();
    _scrollController.dispose();
    _inputFocusNode.dispose();
    _killProcess();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 50),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _appendOutput(String text) {
    setState(() {
      _outputBuffer.write(text);
    });
    _scrollToBottom();
  }

  Future<void> _startProcess() async {
    if (_isRunning) return;

    final prompt = _promptController.text.trim();
    if (prompt.isEmpty) {
      _appendOutput('[ERROR] 프롬프트를 입력하세요\n');
      return;
    }

    setState(() {
      _isRunning = true;
      _status = 'Starting...';
      _outputBuffer.clear();
    });

    try {
      // Python 브릿지 실행
      final scriptPath = _getBridgePath();
      _appendOutput('[INFO] Starting: python $scriptPath\n');
      _appendOutput('[INFO] Prompt: $prompt\n\n');

      _process = await Process.start(
        scriptPath,
        ['-p', prompt, '-w', '3'],
        workingDirectory: _getWorkingDirectory(),
        runInShell: false,
      );

      setState(() {
        _status = 'Running';
      });

      // stdout 스트리밍
      _process!.stdout.transform(utf8.decoder).listen(
        (data) {
          _appendOutput(data);

          // 상태 업데이트
          if (data.contains('[BRIDGE:TASK_COMPLETE]')) {
            setState(() => _status = 'Task Complete');
          } else if (data.contains('[BRIDGE:SEND_PROMPT]')) {
            setState(() => _status = 'Prompt Sent');
          }
        },
        onDone: () {
          setState(() {
            _isRunning = false;
            _status = 'Finished';
          });
          _appendOutput('\n[INFO] Process finished\n');
        },
        onError: (e) {
          _appendOutput('[ERROR] stdout: $e\n');
        },
      );

      // stderr 스트리밍
      _process!.stderr.transform(utf8.decoder).listen(
        (data) {
          _appendOutput('[STDERR] $data');
        },
        onError: (e) {
          _appendOutput('[ERROR] stderr: $e\n');
        },
      );

      // 프로세스 종료 대기
      final exitCode = await _process!.exitCode;
      _appendOutput('[INFO] Exit code: $exitCode\n');
    } catch (e) {
      _appendOutput('[ERROR] Failed to start: $e\n');
      setState(() {
        _isRunning = false;
        _status = 'Error';
      });
    }
  }

  String _getWorkingDirectory() {
    // 실행 파일 위치 기준으로 작업 디렉토리 설정
    final exePath = Platform.resolvedExecutable;
    final exeDir = File(exePath).parent.path;

    // 개발 중일 때는 프로젝트 루트 사용
    if (Directory(r'C:\project\jjiban_flutter').existsSync()) {
      return r'C:\project\jjiban_flutter';
    }
    return exeDir;
  }

  String _getBridgePath() {
    final workDir = _getWorkingDirectory();
    return '$workDir\\claude_terminal\\claude_bridge.exe';
  }

  void _sendInput() {
    if (!_isRunning || _process == null) return;

    final input = _inputController.text.trim();
    if (input.isEmpty) return;

    _process!.stdin.writeln(input);
    _appendOutput('\n[INPUT] $input\n');
    _inputController.clear();
    _inputFocusNode.requestFocus();
  }

  void _killProcess() {
    if (_process != null) {
      try {
        _process!.stdin.writeln('/quit');
      } catch (_) {}
      _process!.kill();
      _process = null;
      setState(() {
        _isRunning = false;
        _status = 'Stopped';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Claude Viewer'),
        backgroundColor: const Color(0xFF2D2D2D),
        actions: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Center(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                decoration: BoxDecoration(
                  color: _isRunning ? Colors.green : Colors.grey,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  _status,
                  style: const TextStyle(fontSize: 12),
                ),
              ),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          // 프롬프트 입력 영역
          Container(
            padding: const EdgeInsets.all(12),
            color: const Color(0xFF2D2D2D),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _promptController,
                    enabled: !_isRunning,
                    decoration: const InputDecoration(
                      hintText: '프롬프트 입력...',
                      border: OutlineInputBorder(),
                      contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    ),
                    onSubmitted: (_) => _startProcess(),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton.icon(
                  onPressed: _isRunning ? _killProcess : _startProcess,
                  icon: Icon(_isRunning ? Icons.stop : Icons.play_arrow),
                  label: Text(_isRunning ? 'Stop' : 'Run'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: _isRunning ? Colors.red : Colors.green,
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                  ),
                ),
              ],
            ),
          ),

          // 터미널 출력 영역
          Expanded(
            child: Container(
              width: double.infinity,
              color: const Color(0xFF1E1E1E),
              padding: const EdgeInsets.all(12),
              child: SingleChildScrollView(
                controller: _scrollController,
                child: SelectableText(
                  _outputBuffer.toString(),
                  style: const TextStyle(
                    fontFamily: 'Consolas',
                    fontSize: 13,
                    color: Colors.white70,
                    height: 1.4,
                  ),
                ),
              ),
            ),
          ),

          // 입력 영역
          Container(
            padding: const EdgeInsets.all(12),
            color: const Color(0xFF2D2D2D),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _inputController,
                    focusNode: _inputFocusNode,
                    enabled: _isRunning,
                    decoration: const InputDecoration(
                      hintText: '명령 입력... (실행 중에만 가능)',
                      border: OutlineInputBorder(),
                      contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    ),
                    onSubmitted: (_) => _sendInput(),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _isRunning ? _sendInput : null,
                  child: const Text('Send'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
